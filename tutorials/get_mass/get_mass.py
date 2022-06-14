#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models import file_source_format
from kittycad.api.file import create_file_mass
from kittycad.models import FileMass
import json

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

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump({
        "id": fm.id,
        "status": fm.status,
        "mass": fm.mass,
    }, f, ensure_ascii=False, indent=4)
