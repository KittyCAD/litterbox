#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models import file_source_format, FileDensity
from kittycad.api.file import create_file_density
import json
import os

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv()

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
content = file.read()
file.close()

fm: FileDensity = create_file_density.sync(
    client=client,
    material_mass=123,
    src_format=file_source_format.FileSourceFormat.OBJ,
    body=content)

print(f"File density: {fm.density}")

partInfo = {
    "title": "output.json",
    "density": fm.density,
}

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
