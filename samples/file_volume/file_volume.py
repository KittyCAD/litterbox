#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models import file_source_format, FileVolume
from kittycad.api.file import create_file_volume
import json
import os

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv()

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
content = file.read()
file.close()

steelDensityPerCubicMillimeter = 0.00785
fm: FileVolume = create_file_volume.sync(
    client=client,
    src_format=file_source_format.FileSourceFormat.OBJ,
    body=content)

print(f"File Volume: {fm.volume}")

partInfo = {
    "title": "output.json",
    "volume": fm.volume,
}

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
