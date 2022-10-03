from typing import List
from pydantic import BaseModel
from sensor import Sensor

import tensorflow as tf
import socketio
import config


class Model(BaseModel):
    sensor_data: List[float]
    model_res: List[int]


device_name, device_channel_name, sampling_rate, samples_per_channel, type = config.load(
    'config.ini')

sensor = Sensor.of(device_name,
                   device_channel_name,
                   sampling_rate,
                   samples_per_channel * 2, type)

# 모델 로딩


async def loop():
    while True:
        datas = await sensor.read(samples_per_channel)

        for idx, data in enumerate(datas):
            await sio.emit('data', {'sensor_id': idx, 'data': data})
            await sio.sleep(0)

        # TODO request to model and get res
        await sio.emit('model', {'result': datas})
        await sio.sleep(0)


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

sio.start_background_task(loop)
