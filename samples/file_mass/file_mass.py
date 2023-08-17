#!/usr/bin/env python3
import json
import os

from kittycad.api.file import create_file_mass
from kittycad.client import ClientFromEnv
from kittycad.models.error import Error
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.file_mass import FileMass
from kittycad.models.unit_density import UnitDensity
from kittycad.models.unit_mass import UnitMass

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

# We divide by 1e+9 here to convert from cubic millimeters to cubic meters.
steelDensityPerCubicMeter = 0.00785 / 1e9
fm = create_file_mass.sync(
    client=client,
    material_density=steelDensityPerCubicMeter,
    src_format=FileImportFormat.OBJ,
    material_density_unit=UnitDensity.KG_M3,
    output_unit=UnitMass.G,
    body=content,
)

if isinstance(fm, Error) or fm is None:
    raise Exception("There was a problem")

fm: FileMass = fm

print(f"File mass (grams): {fm.mass}")

partInfo = {
    "title": "output.json",
    "mass": fm.mass,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
