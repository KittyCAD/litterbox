#!/usr/bin/env python3

from typing import Dict

from kittycad.api.file import create_file_conversion
from kittycad.client import ClientFromEnv
from kittycad.models.base64data import Base64Data
from kittycad.models.error import Error
from kittycad.models.file_conversion import FileConversion
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.file_import_format import FileImportFormat
from kittycad.types import Unset

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Convert a file from OBJ to STL.
# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

result = create_file_conversion.sync(
    client=client,
    body=content,
    src_format=FileImportFormat.OBJ,
    output_format=FileExportFormat.STL,
)

if isinstance(result, Error) or result is None:
    raise Exception("There was a problem")

fc: FileConversion = result

print(f"File conversion id: {fc.id}")
# Try adding your name by changing the text below to
# print("<your-name>, congrats! Your STL conversion was successful:")
print(f"File conversion status: {fc.status}")

if isinstance(fc.outputs, Unset):
    raise Exception("Expected outputs to be set")

outputs: Dict[str, Base64Data] = fc.outputs

if len(outputs) != 1:
    raise Exception("Expected one output file")

# LITTERBOX-START-NON-EDITABLE-SECTION
for _, output in outputs.items():
    output_file_path = "./output.stl"
    print(f"Saving output to {output_file_path}")
    output_file = open(output_file_path, "wb")
    output_file.write(output.get_decoded())
    output_file.close()
