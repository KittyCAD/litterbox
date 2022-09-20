#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models import file_source_format, FileMass
from kittycad.api.file import create_file_mass
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
fm: FileMass = create_file_mass.sync(
    client=client,
    material_density=steelDensityPerCubicMillimeter,
    src_format=file_source_format.FileSourceFormat.OBJ,
    body=content)

print(f"File mass (grams): {fm.mass}")

partInfo = {
    "title": "output.json",
    "mass": fm.mass,
}

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
