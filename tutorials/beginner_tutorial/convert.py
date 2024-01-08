from typing import Dict, Optional, Union

from kittycad.api.file import create_file_conversion
from kittycad.client import ClientFromEnv
from kittycad.models import Error, FileConversion
from kittycad.models.base64data import Base64Data
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.file_import_format import FileImportFormat
from kittycad.types import Unset

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.


def convertOBJtoSTL():
    client = ClientFromEnv(timeout=500, verify_ssl=True)

    # Convert a file from OBJ to STL.
    # Read in the contents of the file.
    file = open("./dodecahedron.obj", "rb")
    content = file.read()
    file.close()

    result: Optional[Union[Error, FileConversion]] = create_file_conversion.sync(
        client=client,
        body=content,
        src_format=FileImportFormat.OBJ,
        output_format=FileExportFormat.STL,
    )

    if isinstance(result, Error) or result is None:
        raise Exception("There was a problem")

    body: FileConversion = result

    if isinstance(body.outputs, Unset):
        raise Exception("Expected outputs to be set")

    outputs: Dict[str, Base64Data] = body.outputs

    for _, output in outputs.items():
        output_file_path = "./output.stl"
        print(f"Saving output to {output_file_path}")
        output_file = open(output_file_path, "wb")
        output_file.write(output.get_decoded())
        output_file.close()

    return body


convertOBJtoSTL()
