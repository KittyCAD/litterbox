from kittycad.client import ClientFromEnv
from kittycad.api.meta import ping

pong = ping.sync(client=ClientFromEnv(timeout=500, verify_ssl=True))
print(pong)
