#!/usr/bin/env python3

from typing import Tuple

from kittycad.api.file import create_file_conversion_with_base64_helper
from kittycad.client import ClientFromEnv
from kittycad.models.error import Error
from kittycad.models.file_conversion import FileConversion
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.file_import_format import FileImportFormat

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Convert a file from OBJ to STL.
# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

result = create_file_conversion_with_base64_helper.sync(
    client=client,
    body=content,
    src_format=FileImportFormat.OBJ,
    output_format=FileExportFormat.STL,
)

if isinstance(result, Error) or result is None:
    raise Exception("There was a problem")

r: Tuple[FileConversion, bytes] = result  # type: ignore

# Get the bytes of the output file.
b: bytes = r[1]
fc: FileConversion = r[0]

print(f"File conversion id: {fc.id}")
# Try adding your name by changing the text below to
# print("<your-name>, congrats! Your STL conversion was successful:")
print(f"File conversion status: {fc.status}")

# LITTERBOX-START-NON-EDITABLE-SECTION
output_file_path = "./output.stl"
print(f"Saving output to {output_file_path}")
output_file = open(output_file_path, "wb")
output_file.write(b)
output_file.close()
