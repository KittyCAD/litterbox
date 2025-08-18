#!/usr/bin/env python3


from typing import Dict

from kittycad import KittyCAD, KittyCADAPIError
from kittycad.models.base64data import Base64Data
from kittycad.models.file_conversion import FileConversion
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.file_import_format import FileImportFormat
from kittycad.types import Unset

# Create a new client with your token parsed from the environment variable:
#   ZOO_API_TOKEN.
client = KittyCAD(timeout=500, verify_ssl=True)

# Convert a file from OBJ to STL.
# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

try:
    result = client.file.create_file_conversion(
        body=content,
        src_format=FileImportFormat.OBJ,
        output_format=FileExportFormat.STL,
    )
except KittyCADAPIError as e:
    raise Exception(f"There was a problem: {e}")

fc: FileConversion = result

print(f"File conversion id: {fc.id}")
print(f"File conversion status: {fc.status}")

if isinstance(fc.outputs, Unset):
    raise Exception("Expected outputs to be set")

if fc.outputs is None:
    raise Exception("Expected outputs to be set")

outputs: Dict[str, Base64Data] = fc.outputs

if len(outputs) != 1:
    raise Exception("Expected one output file")

# LITTERBOX-START-NON-EDITABLE-SECTION
for _, output in outputs.items():
    output_file_path = "./output.stl"
    print(f"Saving output to {output_file_path}")
    output_file = open(output_file_path, "wb")
    output_file.write(output)
    output_file.close()
