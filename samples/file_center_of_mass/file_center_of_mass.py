#!/usr/bin/env python3

import json
import os

from kittycad import KittyCAD, KittyCADAPIError
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.unit_length import UnitLength

# Create a new client with your token parsed from the environment variable:
#   ZOO_API_TOKEN.
client = KittyCAD(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./seesaw.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

try:
    fm = client.file.create_file_center_of_mass(
        output_unit=UnitLength.M,
        src_format=FileImportFormat.OBJ,
        body=content,
    )
except KittyCADAPIError as e:
    raise Exception(f"There was a problem: {e}")

if fm.center_of_mass is None:
    raise Exception("There was a problem")

print(f"File center of mass (meters): {fm.center_of_mass}")

partInfo = {
    "title": "output.json",
    "center_of_mass": fm.center_of_mass.model_dump(),
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./seesaw.obj ./output.obj")
