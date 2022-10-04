from sensor import Sensor
import asyncio

a = Sensor.vib("cDAQ1Mod1", "ai0:3", 51200, 51200)


async def doing():
    res = await a.read()
    print(len(res))
    print(len(res[0]))

asyncio.run(doing())
