from kittycad.client import ClientFromEnv
from kittycad.models import Pong
from kittycad.api.meta import ping

pong: Pong = ping.sync(client=ClientFromEnv())
print(pong)
