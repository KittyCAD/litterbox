#!/usr/bin/env python3

from kittycad.api.meta import ping
from kittycad.client import ClientFromEnv

pong = ping.sync(client=ClientFromEnv(timeout=500, verify_ssl=True))
print(pong)
