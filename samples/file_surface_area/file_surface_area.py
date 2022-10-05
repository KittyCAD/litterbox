#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.models.file3_d_import_format import File3DImportFormat
from kittycad.api.file import create_file_surface_area
from kittycad.models.error import Error
import json
import os

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

fm = create_file_surface_area.sync(client=client,
                                   src_format=File3DImportFormat.OBJ,
                                   body=content)

if isinstance(fm, Error) or fm == None:
    raise Exception("There was a problem")

print(f"File surface area: {fm.surface_area}")

partInfo = {
    "title": "output.json",
    "surface_area": fm.surface_area,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
