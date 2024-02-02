import json
import os
import uuid

from kittycad.client import ClientFromEnv

from kittycad.api.modeling import modeling_commands_ws
from kittycad.models import (
    ImageFormat,
    ModelingCmd,
    ModelingCmdId,
    WebSocketRequest,
)
from kittycad.models.path_segment import PathSegment, line
from kittycad.models.modeling_cmd import (
    default_camera_look_at,
    start_path,
    take_snapshot,
    extend_path,
    move_path_pen,
    extrude,
    close_path,
)
from kittycad.models.web_socket_request import modeling_cmd_req

def make_cube():
    
    # Create our client.
    client = ClientFromEnv()

    # Create a unique id for the sketch path.
    sketch_path_id = uuid.uuid4()

    # Connect to the websocket.
    with modeling_commands_ws.WebSocket(
        client=client,
        fps=30,
        unlocked_framerate=False,
        video_res_height=360,
        video_res_width=480,
        webrtc=False,
    ) as websocket:

    #Draw a sqaure

        # Start the Path
        websocket.send(WebSocketRequest(
            modeling_cmd_req(cmd=ModelingCmd(start_path()), cmd_id=ModelingCmdId(sketch_path_id)),
        ))

        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(
                    move_path_pen(
                        path=str(sketch_path_id), 
                        to={
                            "x": -5,
                            "y": -5,
                            "z": 0,
                        }
                    )
                ), 
                cmd_id=ModelingCmdId(uuid.uuid4()))))

        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(
                    extend_path(
                        path=str(sketch_path_id),
                        segment=line(
                            end={
                                "x": 10,
                                "y": 0,
                                "z": 0,
                            },
                            relative=True,
                        )
                    )), 
                cmd_id=ModelingCmdId(uuid.uuid4())
            )
        ))

        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(
                    extend_path(
                        path=str(sketch_path_id),
                        segment=line(
                            end={
                                "x": 0,
                                "y": 10,
                                "z": 0,
                            },
                            relative=True,
                        )
                    )), 
                cmd_id=ModelingCmdId(uuid.uuid4())
            )
        ))

        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(
                    extend_path(
                        path=str(sketch_path_id),
                        segment=line(
                            end={
                                "x": -10,
                                "y": 0,
                                "z": 0,
                            },
                            relative=True,
                        )
                    )), 
                cmd_id=ModelingCmdId(uuid.uuid4())
            )
        ))

        # Close the sketch
        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(
                    close_path(
                        path_id=ModelingCmdId(sketch_path_id)
                    )
                ),
                cmd_id=ModelingCmdId(uuid.uuid4())
            )
        ))

        # Extrude the square into a cube
        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(
                    extrude(
                        cap=True,
                        distance=10,
                        target=ModelingCmdId(sketch_path_id),
                    )
                ), 
                cmd_id=ModelingCmdId(uuid.uuid4())
            )
        ))

        # Get the messages.
        while True:
                message = websocket.recv()
                print(json.dumps(message.model_dump_json(), indent=4, sort_keys=True))
                break

        # Orient the camera.
        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(default_camera_look_at(
                    center = {"x": 0, "y": 0, "z": 0},
                    up = {"x": 0, "y": 0, "z": 1},
                    vantage = {"x": 20, "y": 20, "z": 20},
                )),
                cmd_id=ModelingCmdId(uuid.uuid4())
            )
        ))

        # Take a snapshot.
        websocket.send(WebSocketRequest(
            modeling_cmd_req(
                cmd=ModelingCmd(take_snapshot(format=ImageFormat.PNG)),
                cmd_id=ModelingCmdId(uuid.uuid4())
            )
        ))
        
        png_contents = b""
        for message in websocket:
            message_dict = message.model_dump()
            print(message_dict)
            if (
                message_dict["resp"]["data"]["modeling_response"]["type"] == "take_snapshot"
            ):
                png_contents = message_dict["resp"]["data"]["modeling_response"][
                    "data"
                ]["contents"].get_decoded()
                break

        # Save the contents to a file.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        png_path = os.path.join(dir_path, "snapshot.png")
        print(png_path)
        with open(png_path, "wb") as f:
            f.write(png_contents)

        # Ensure the file is not empty.
        assert len(png_contents) > 0

        # Ensure the file exists.
        assert os.path.exists(png_path)

make_cube()