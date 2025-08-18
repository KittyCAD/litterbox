#!/usr/bin/env python3

from kittycad import KittyCAD

client = KittyCAD(timeout=500, verify_ssl=True)
pong = client.meta.ping()
print(pong)
