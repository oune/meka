from typing import List
from pydantic import BaseModel
import pandas as pd
import socketio
import asyncio

from sensor import Sensor
import config

device_name, device_channel_name, sampling_rate, samples_per_channel, type = config.load(
    'config.ini')

sensor = Sensor.of(device_name, device_channel_name,
                   sampling_rate, samples_per_channel, type)

sio = socketio.AsyncServer()


@sio.on('setting')
def another_event(sid, data):
    pass


async def roop():
    datas = await sensor.read()
    sio.emit('data', {'data': datas})
    # TODO req model
    # TODO emit 'model_res'


asyncio.run(roop())
