#!/usr/bin/env python3

import json
import os

from kittycad.api.file import create_file_center_of_mass
from kittycad.client import ClientFromEnv
from kittycad.models.error import Error
from kittycad.models.file_import_format import FileImportFormat
from kittycad.models.unit_length import UnitLength

# Create a new client with your token parsed from the environment variable:
#   KITTYCAD_API_TOKEN.
client = ClientFromEnv(timeout=500, verify_ssl=True)

# Read in the contents of the file.
file = open("./seesaw.obj", "rb")
# LITTERBOX-END-NON-EDITABLE-SECTION
content = file.read()
file.close()

fm = create_file_center_of_mass.sync(
    client=client,
    output_unit=UnitLength.M,
    src_format=FileImportFormat.OBJ,
    body=content,
)

if isinstance(fm, Error) or fm is None:
    raise Exception("There was a problem")

print(f"File center of mass (meters): {fm.center_of_mass}")

partInfo = {
    "title": "output.json",
    "center_of_mass": fm.center_of_mass,
}

# LITTERBOX-START-NON-EDITABLE-SECTION
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(partInfo, f, ensure_ascii=False, indent=4)
os.system("cp ./seesaw.obj ./output.obj")
