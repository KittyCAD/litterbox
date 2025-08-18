from typing import Dict

from kittycad import KittyCAD, KittyCADAPIError
from kittycad.models.base64data import Base64Data
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.file_import_format import FileImportFormat
from kittycad.types import Unset


# Create a new function to convert an OBJ file to an STL file.
def convertOBJtoSTL():
    # Create a new client with your token parsed from the environment variable (ZOO_API_TOKEN)
    client = KittyCAD(timeout=500, verify_ssl=True)

    # Read in the contents of the file.
    file = open("./dodecahedron.obj", "rb")
    content = file.read()
    file.close()

    # Call the create_file_conversion function with the required parameters: client, body, src_format, and output_format.

    try:
        body = client.file.create_file_conversion(
            body=content,  # The contents of the file you read in.
            src_format=FileImportFormat.OBJ,  # The format of the file you read in.
            output_format=FileExportFormat.STL,  # The format you want to convert to.
        )
    except KittyCADAPIError as e:
        raise Exception(f"There was a problem: {e}")
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
