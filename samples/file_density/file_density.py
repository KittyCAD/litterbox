#!/usr/bin/env python3

import json
import os

from kittycad import KittyCAD, KittyCADAPIError
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.unit_density import UnitDensity
from kittycad.models.unit_mass import UnitMass

# Create a new client with your token parsed from the environment variable:
#   ZOO_API_TOKEN.
client = KittyCAD(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

try:
    fm = client.file.create_file_density(
        material_mass=123,
        material_mass_unit=UnitMass.G,
        output_unit=UnitDensity.KG_M3,
        src_format=FileImportFormat.OBJ,
        body=content,
    )
except KittyCADAPIError as e:
    raise Exception(f"There was a problem: {e}")

print(f"File density (kg/m^3): {fm.density}")

partInfo = {
    "title": "output.json",
    "density": fm.density,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
