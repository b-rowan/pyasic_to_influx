import asyncio
import json

import pyasic
from decouple import Config
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

conf = Config(".env")
SECRET = conf.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN", "secret")
ORG = conf.get("DOCKER_INFLUXDB_INIT_ORG", "admin")

with open("settings.json", "r") as f:
    SETTINGS = json.loads(f.read())


async def update_data(ip: str):
    miner = await pyasic.get_miner(ip)
    return await miner.get_data()


async def write_data(data: pyasic.MinerData):
    async with InfluxDBClientAsync("http://influx:8086", token=SECRET, org=ORG) as c:
        await c.write_api().write("miners", record=data.as_influxdb("miners"))


async def main():
    while True:
        data = await asyncio.gather(*[update_data(ip) for ip in SETTINGS.get("ips", [])])
        await asyncio.gather(*[write_data(dp) for dp in data])
        await asyncio.sleep(SETTINGS.get("sleep_time", 5))

if __name__ == '__main__':
    asyncio.run(main())