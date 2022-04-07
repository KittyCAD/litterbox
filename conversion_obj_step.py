#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models import FileConversionWithOutput, FileConversionSourceFormat, FileConversionOutputFormat
from kittycad.api.file import create_file_conversion_with_base64_helper
import json

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv()

# Convert a file from OBJ to STEP.
# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
content = file.read()
file.close()

fc: FileConversionWithOutput = create_file_conversion_with_base64_helper.sync(client=client, body=content, source_format=FileConversionSourceFormat.OBJ, output_format=FileConversionOutputFormat.STEP)

print(f"File conversion id: {fc.id}")
print(f"File conversion status: {fc.status}")

output_file_path = "./output.step"
print(f"Saving output to {output_file_path}")
output_file = open(output_file_path ,"wb")
output_file.write(fc.output)
output_file.close()
