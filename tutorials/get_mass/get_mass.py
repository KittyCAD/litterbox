#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models import file_source_format
from kittycad.api.file import create_file_mass
from kittycad.models import FileMass

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv()

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
content = file.read()
file.close()

print(file_source_format.FileSourceFormat.OBJ)

fm: FileMass = create_file_mass.sync(
    client=client,
    material_density=5.0,
    src_format=file_source_format.FileSourceFormat.OBJ,
    body=content)

print(f"File mass: {fm}")
