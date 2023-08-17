#!/usr/bin/env python3

import json
import os

from kittycad.api.file import create_file_surface_area
from kittycad.client import ClientFromEnv
from kittycad.models.error import Error
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.file_surface_area import FileSurfaceArea
from kittycad.models.unit_area import UnitArea

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

fm = create_file_surface_area.sync(
    client=client,
    output_unit=UnitArea.M2,
    src_format=FileImportFormat.OBJ,
    body=content,
)

if isinstance(fm, Error) or fm is None:
    raise Exception("There was a problem")

fm: FileSurfaceArea = fm

print(f"File surface area (m^2): {fm.surface_area}")

partInfo = {
    "title": "output.json",
    "surface_area": fm.surface_area,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
