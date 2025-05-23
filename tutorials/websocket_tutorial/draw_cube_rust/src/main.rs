use color_eyre::{
    eyre::{bail, Context, Error},
    Result,
};
use futures::{
    stream::{SplitSink, SplitStream},
    SinkExt, StreamExt,
};
use kittycad::types::{
    FailureWebSocketResponse, ModelingCmd, OkModelingCmdResponse, OkWebSocketResponseData,
    PathSegment, Point3D, SuccessWebSocketResponse, WebSocketRequest,
};
use reqwest::Upgraded;
use std::{env, io::Cursor, time::Duration};
use tokio::time::timeout;
use tokio_tungstenite::{tungstenite::Message as WsMsg, WebSocketStream};
use uuid::Uuid;

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<()> {
    // Set up the API client.
    let kittycad_api_token = env::var("ZOO_API_TOKEN").context("You must set $ZOO_API_TOKEN")?;
    let kittycad_api_client = kittycad::Client::new(kittycad_api_token);

    // Where should the final PNG be saved?
    let img_output_path = env::var("IMAGE_OUTPUT_PATH").unwrap_or_else(|_| "model.png".to_owned());

    // Establish a WebSocket connection to KittyCAD's modeling API.
    let ws = kittycad_api_client
        .modeling()
        .commands_ws(
            Some(30),
            None,
            None,
            None,
            Some(true),
            Some(false),
            Some(480),
            Some(640),
            Some(false),
        )
        .await
        .context("Could not open WebSocket to KittyCAD Modeling API")?;

    // Now that we have a WebSocket connection, we can split it into two ends:
    // one for writing to and one for reading from.
    let (write, read) = tokio_tungstenite::WebSocketStream::from_raw_socket(
        ws.0,
        tokio_tungstenite::tungstenite::protocol::Role::Client,
        None,
    )
    .await
    .split();

    // First, send all commands to the API, to draw a cube.
    // Then, read all responses from the API, to download the cube as a PNG.
    draw_cube(write, 10.0).await?;
    export_png(read, img_output_path).await
}

/// Send modeling commands to the KittyCAD API.
/// We're going to draw a cube and export it as a PNG.
async fn draw_cube(
    mut write_to_ws: SplitSink<WebSocketStream<Upgraded>, WsMsg>,
    width: f64,
) -> Result<()> {
    // All messages to the KittyCAD Modeling API will be sent over the WebSocket as Text.
    // The text will contain JSON representing a `ModelingCmdReq`.
    // This takes in a command and its ID, and makes a WebSocket message containing that command.
    fn to_msg(cmd: ModelingCmd, cmd_id: Uuid) -> WsMsg {
        WsMsg::Text(
            serde_json::to_string(&WebSocketRequest::ModelingCmdReq { cmd, cmd_id }).unwrap(),
        )
    }

    // Now the WebSocket is set up and ready to use!
    // We can start sending commands.

    // Create a new empty path.
    let path_id = Uuid::new_v4();
    write_to_ws
        .send(to_msg(ModelingCmd::StartPath {}, path_id))
        .await?;

    // Add four lines to the path,
    // in the shape of a square.
    // First, start the path at the first corner.
    let start = Point3D {
        x: -width,
        y: -width,
        z: -width,
    };
    write_to_ws
        .send(to_msg(
            ModelingCmd::MovePathPen {
                path: path_id,
                to: start,
            },
            Uuid::new_v4(),
        ))
        .await?;

    // Now extend the path to each corner, and back to the start.
    let points = [
        Point3D {
            x: width,
            y: -width,
            z: -width,
        },
        Point3D {
            x: width,
            y: width,
            z: -width,
        },
        Point3D {
            x: -width,
            y: width,
            z: -width,
        },
        start,
    ];
    for point in points {
        write_to_ws
            .send(to_msg(
                ModelingCmd::ExtendPath {
                    path: path_id,
                    segment: PathSegment::Line {
                        end: point,
                        relative: false,
                    },
                },
                Uuid::new_v4(),
            ))
            .await?;
    }

    // Extrude the square into a cube.
    write_to_ws
        .send(to_msg(ModelingCmd::ClosePath { path_id }, Uuid::new_v4()))
        .await?;
    write_to_ws
        .send(to_msg(
            ModelingCmd::Extrude {
                distance: width * 2.0,
                target: path_id,
                faces: Default::default(),
            },
            Uuid::new_v4(),
        ))
        .await?;

    // Export the model as a PNG.
    write_to_ws
        .send(to_msg(
            ModelingCmd::TakeSnapshot {
                format: kittycad::types::ImageFormat::Png,
            },
            Uuid::new_v4(),
        ))
        .await?;

    // Finish sending
    drop(write_to_ws);
    Ok(())
}

/// Read WebSocket messages until we receive the PNG from the API.
/// Then save it to the local filesystem.
async fn export_png(
    mut read_from_ws: SplitStream<WebSocketStream<Upgraded>>,
    img_output_path: String,
) -> Result<()> {
    /// Given the text from a WebSocket, deserialize its JSON.
    /// Returns OK if the WebSocket's JSON represents a successful response.
    /// Returns an error if the WebSocket's JSON represented a failure response.
    fn decode_websocket_text(
        text: &str,
    ) -> Result<std::result::Result<OkWebSocketResponseData, FailureWebSocketResponse>> {
        let resp: WebSocketResponse = serde_json::from_str(text)?;
        match resp {
            WebSocketResponse::Success(s) => {
                assert!(s.success);
                Ok(Ok(s.resp))
            }
            WebSocketResponse::Failure(f) => {
                assert!(!f.success);
                Ok(Err(f))
            }
        }
    }

    /// Find the text in a WebSocket message, if there's any.
    fn text_from_ws(msg: WsMsg) -> Option<String> {
        match msg {
            WsMsg::Text(text) => Some(text),
            _ => None,
        }
    }

    // Get Websocket messages from API server
    let server_responses = async move {
        while let Some(msg) = read_from_ws.next().await {
            // We're looking for a WebSocket response with text.
            // Ignore any other type of WebSocket messages.
            let Some(resp) = text_from_ws(msg?) else {
                continue;
            };
            // What did the WebSocket response contain?
            // It should either match the KittyCAD successful response schema, or the failed response schema.
            match decode_websocket_text(&resp)? {
                // Success!
                Ok(OkWebSocketResponseData::Modeling { modeling_response }) => {
                    match modeling_response {
                        OkModelingCmdResponse::Empty {} => {}
                        OkModelingCmdResponse::TakeSnapshot { data } => {
                            save_image(data.contents.into(), &img_output_path)?;
                            break;
                        }
                        _ => {}
                    }
                }
                // Success, but not a modeling response
                Ok(_) => {}
                // Failure
                Err(failure) => bail!("KittyCAD API responded with an error: {failure:?}"),
            }
        }
        Ok::<_, Error>(())
    };
    timeout(Duration::from_secs(10), server_responses).await??;
    Ok(())
}

fn save_image(contents: Vec<u8>, output_path: &str) -> Result<()> {
    let mut img = image::ImageReader::new(Cursor::new(contents));
    img.set_format(image::ImageFormat::Png);
    let img = img.decode()?;
    img.save(output_path)?;
    Ok(())
}

/// The WebSocket responses coming from the server.
#[derive(serde::Deserialize)]
#[serde(untagged)]
enum WebSocketResponse {
    Success(SuccessWebSocketResponse),
    Failure(FailureWebSocketResponse),
}
