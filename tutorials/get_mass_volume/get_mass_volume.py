#!/usr/bin/env python3

import json
import os

from kittycad import KittyCAD, KittyCADAPIError
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.unit_density import UnitDensity
from kittycad.models.unit_mass import UnitMass
from kittycad.models.unit_volume import UnitVolume

# Create a new client with your token parsed from the environment variable:
#   ZOO_API_TOKEN.
client = KittyCAD(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

# We divide by 1e+9 here to convert from cubic millimeters to cubic meters.
steelDensityPerCubicMeter = 0.00785 / 1e9
try:
    fm = client.file.create_file_mass(
        material_density=steelDensityPerCubicMeter,
        src_format=FileImportFormat.OBJ,
        material_density_unit=UnitDensity.KG_M3,
        output_unit=UnitMass.G,
        body=content,
    )
except KittyCADAPIError as e:
    raise Exception(f"There was a problem with mass calculation: {e}")

try:
    fv = client.file.create_file_volume(
        src_format=FileImportFormat.OBJ,
        output_unit=UnitVolume.M3,
        body=content,
    )
except KittyCADAPIError as e:
    raise Exception(f"There was a problem with volume calculation: {e}")

print(f"File mass (grams): {fm.mass}")
print(f"File volume (m^3): {fv.volume}")

partInfo = {
    "title": "output.json",
    "volume": fv.volume,
    "mass": fm.mass,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
