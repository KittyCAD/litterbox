#!/usr/bin/env python3
import json
import os

from kittycad.api.file import create_file_volume
from kittycad.client import ClientFromEnv
from kittycad.models.error import Error
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.file_volume import FileVolume
from kittycad.models.unit_volume import UnitVolume

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./ORIGINALVOXEL-3.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

fv = create_file_volume.sync(
    client=client,
    output_unit=UnitVolume.M3,
    src_format=FileImportFormat.OBJ,
    body=content,
)

if isinstance(fv, Error) or fv is None:
    raise Exception("There was a problem")

fv: FileVolume = fv

print(f"File volume (m^3): {fv.volume}")

partInfo = {
    "title": "output.json",
    "volume": fv.volume,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./ORIGINALVOXEL-3.obj ./output.obj")
