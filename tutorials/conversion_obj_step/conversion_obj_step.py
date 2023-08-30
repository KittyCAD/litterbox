#!/usr/bin/env python3


from kittycad.api.file import create_file_conversion
from kittycad.client import ClientFromEnv
from kittycad.models.error import Error
from kittycad.models.file_conversion import FileConversion
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.file_import_format import FileImportFormat

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Convert a file from OBJ to STEP.
# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
content = file.read()
file.close()

result = create_file_conversion.sync(
    client=client,
    body=content,
    src_format=FileImportFormat.OBJ,
    output_format=FileExportFormat.STEP,
)

if isinstance(result, Error) or result is None:
    raise Exception("There was a problem")

fc: FileConversion = result

print(f"File conversion id: {fc.id}")
print(f"File conversion status: {fc.status}")

if fc.outputs.length != 1:
    raise Exception("Expected one output file")

# LITTERBOX-START-NON-EDITABLE-SECTION
for _, output in fc.outputs.items():
    output_file_path = "./output.step"
    print(f"Saving output to {output_file_path}")
    output_file = open(output_file_path, "wb")
    output_file.write(output.get_decoded())
    output_file.close()
