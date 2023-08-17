#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.api.file import create_file_mass, create_file_volume
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.unit_volume import UnitVolume
from kittycad.models.unit_mass import UnitMass
from kittycad.models.unit_density import UnitDensity
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

# We divide by 1e+9 here to convert from cubic millimeters to cubic meters.
steelDensityPerCubicMeter = 0.00785 / 1e+9
fm = create_file_mass.sync(client=client,
                           material_density=steelDensityPerCubicMeter,
                           src_format=FileImportFormat.OBJ,
                           material_density_unit=UnitDensity.KG_M3,
                           output_unit=UnitMass.G,
                           body=content)
fv = create_file_volume.sync(client=client,
                             src_format=FileImportFormat.OBJ,
                             output_unit=UnitVolume.M3,
                             body=content)

if isinstance(fm, Error) or fm == None:
    raise Exception("There was a problem with mass calculation")
if isinstance(fv, Error) or fv == None:
    raise Exception("There was a problem with volume calculation")

print(f"File mass (grams): {fm.mass}")
print(f"File volume (m^3): {fv.volume}")

partInfo = {
    "title": "output.json",
    "volume": fv.volume,
    "mass": fm.mass,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
