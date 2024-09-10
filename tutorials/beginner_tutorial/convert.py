from typing import Dict, Optional, Union

from kittycad.api.file import create_file_conversion
from kittycad.client import ClientFromEnv
from kittycad.models import Error, FileConversion
from kittycad.models.base64data import Base64Data
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.file_import_format import FileImportFormat
from kittycad.types import Unset


# Create a new function to convert an OBJ file to an STL file.
def convertOBJtoSTL():
    # Create a new client with your token parsed from the environment variable (KITTYCAD_API_TOKEN)
    client = ClientFromEnv(timeout=500, verify_ssl=True)

    # Read in the contents of the file.
    file = open("./dodecahedron.obj", "rb")
    content = file.read()
    file.close()

    # Call the create_file_conversion function with the required parameters: client, body, src_format, and output_format.

    result: Optional[Union[Error, FileConversion]] = create_file_conversion.sync(
        client=client,  # The client you created above.
        body=content,  # The contents of the file you read in.
        src_format=FileImportFormat.OBJ,  # The format of the file you read in.
        output_format=FileExportFormat.STL,  # The format you want to convert to.
    )

    # Check if the result is an error or None.
    if isinstance(result, Error) or result is None:
        raise Exception("There was a problem")

    body: FileConversion = result
    if isinstance(body.outputs, Unset):
        raise Exception("Expected outputs to be set")

    # Loop through the outputs and save them to a file.
    outputs: Dict[str, Base64Data] = body.outputs

    for _, output in outputs.items():
        output_file_path = "./dodecahedron.stl"
        print(f"Saving output to {output_file_path}")
        output_file = open(output_file_path, "wb")
        output_file.write(output)
        output_file.close()
    return body


convertOBJtoSTL()
