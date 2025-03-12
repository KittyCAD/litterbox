import os
import uuid

from kittycad.api.modeling import modeling_commands_ws
from kittycad.client import ClientFromEnv
from kittycad.models import (
    Axis,
    AxisDirectionPair,
    Direction,
    ImageFormat,
    ImportFile,
    InputFormat3d,
    ModelingCmd,
    ModelingCmdId,
    System,
    UnitLength,
    WebSocketRequest,
)
from kittycad.models.input_format3d import OptionObj
from kittycad.models.modeling_cmd import (
    OptionDefaultCameraFocusOn,
    OptionImportFiles,
    OptionTakeSnapshot,
)
from kittycad.models.web_socket_request import OptionModelingCmdReq


def test_ws_import():
    # Create our client.
    client = ClientFromEnv()

    # Connect to the websocket.
    with modeling_commands_ws.WebSocket(
        client=client,
        fps=30,
        unlocked_framerate=False,
        video_res_height=360,
        video_res_width=480,
        webrtc=False,
    ) as websocket:
        # read the content of the file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        file_name = "dodecahedron.obj"
        file = open(os.path.join(dir_path, file_name), "rb")
        content = file.read()
        file.close()
        cmd_id = uuid.uuid4()
        ImportFile(data=content, path=file_name)
        # form the request
        req = WebSocketRequest(
            OptionModelingCmdReq(
                cmd=ModelingCmd(
                    OptionImportFiles(
                        files=[ImportFile(data=content, path=file_name)],
                        format=InputFormat3d(
                            OptionObj(
                                units=UnitLength.M,
                                coords=System(
                                    forward=AxisDirectionPair(
                                        axis=Axis.Y, direction=Direction.NEGATIVE
                                    ),
                                    up=AxisDirectionPair(
                                        axis=Axis.Z, direction=Direction.POSITIVE
                                    ),
                                ),
                            )
                        ),
                    )
                ),
                cmd_id=ModelingCmdId(cmd_id),
            )
        )
        # Import files request must be sent as binary, because the file contents might be binary.
        websocket.send_binary(req)

        # Get the success message.
        object_id = ""
        for message in websocket:
            message_dict = message.model_dump()
            if message_dict["success"] is not True:
                raise Exception(message_dict)
            elif message_dict["resp"]["type"] != "modeling":
                continue
            elif (
                message_dict["resp"]["data"]["modeling_response"]["type"]
                != "import_files"
            ):
                # We have a modeling command response.
                # Make sure its the import files response.
                raise Exception(message_dict)
            else:
                # Okay we have the import files response.
                # Break since now we know it was a success.
                object_id = str(
                    message_dict["resp"]["data"]["modeling_response"]["data"][
                        "object_id"
                    ]
                )
                break

        # Now we want to focus on the object.
        cmd_id = uuid.uuid4()
        # form the request
        req = WebSocketRequest(
            OptionModelingCmdReq(
                cmd=ModelingCmd(OptionDefaultCameraFocusOn(uuid=object_id)),
                cmd_id=ModelingCmdId(cmd_id),
            )
        )
        websocket.send(req)

        # Get the success message.
        for message in websocket:
            message_dict = message.model_dump()
            if message_dict["success"] is not True:
                raise Exception(message_dict)
            elif message_dict["resp"]["type"] != "modeling":
                continue
            elif message_dict["request_id"] == str(cmd_id):
                # We got a success response for our cmd.
                break
            else:
                raise Exception(message_dict)

        # Now we want to snapshot as a png.
        cmd_id = uuid.uuid4()
        # form the request
        req = WebSocketRequest(
            OptionModelingCmdReq(
                cmd=ModelingCmd(OptionTakeSnapshot(format=ImageFormat.PNG)),
                cmd_id=ModelingCmdId(cmd_id),
            )
        )
        websocket.send(req)

        # Get the success message.
        png_contents = b""
        for message in websocket:
            message_dict = message.model_dump()
            if message_dict["success"] is not True:
                raise Exception(message_dict)
            elif message_dict["resp"]["type"] != "modeling":
                continue
            elif (
                message_dict["resp"]["data"]["modeling_response"]["type"]
                != "take_snapshot"
            ):
                # Make sure its the correct response.
                raise Exception(message_dict)
            else:
                print(message_dict)
                # Okay we have the snapshot response.
                # Break since now we know it was a success.
                png_contents = message_dict["resp"]["data"]["modeling_response"][
                    "data"
                ]["contents"]
                break

        # Save the contents to a file.
        png_path = os.path.join(dir_path, "snapshot.png")
        with open(png_path, "wb") as f:
            f.write(png_contents)

        # Ensure the file is not empty.
        assert len(png_contents) > 0

        # Ensure the file exists.
        assert os.path.exists(png_path)


test_ws_import()
