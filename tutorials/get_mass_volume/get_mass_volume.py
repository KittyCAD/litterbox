#!/usr/bin/env python3
from kittycad.client import ClientFromEnv
from kittycad.api.file import create_file_mass, create_file_volume
from kittycad.models.file3_d_import_format import File3DImportFormat
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

steelDensityPerCubicMillimeter = 0.00785
fm = create_file_mass.sync(client=client,
                           material_density=steelDensityPerCubicMillimeter,
                           src_format=File3DImportFormat.OBJ,
                           body=content)
fv = create_file_volume.sync(client=client,
                             src_format=File3DImportFormat.OBJ,
                             body=content)

if isinstance(fm, Error) or fm == None:
    raise Exception("There was a problem with mass calculation")
if isinstance(fv, Error) or fv == None:
    raise Exception("There was a problem with volume calculation")

print(f"File mass (grams): {fm.mass}")
print(f"File volume (mm^3): {fv.volume}")

partInfo = {
    "title": "output.json",
    "volume": fv.volume,
    "mass": fm.mass,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
