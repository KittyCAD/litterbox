#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models import file_source_format
from kittycad.api.file import create_file_volume
from kittycad.models import FileVolume

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv()

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
content = file.read()
file.close()

print(file_source_format.FileSourceFormat.OBJ)

fv: FileVolume = create_file_volume.sync(
    client=client,
    src_format=file_source_format.FileSourceFormat.OBJ,
    body=content)

print(f"File volume: {fv}")
