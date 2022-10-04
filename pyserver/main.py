from typing import List
from pydantic import BaseModel
from sensor import Sensor
from time import ctime, time
from Inference.inference import inference, model, scaler, threshold

import tensorflow as tf
import socketio
import config


class Model(BaseModel):
    sensor_data: List[float]
    model_res: List[int]


device_name, device_channel_name, sampling_rate, samples_per_channel, modeltype = config.load(
    'config.ini')

sensor = Sensor.of(device_name,
                   device_channel_name,
                   sampling_rate,
                   samples_per_channel * 2, modeltype)

# 모델 로딩


async def loop():
    while True:
        datas = await sensor.read(samples_per_channel, 30.0)

        for idx, data in enumerate(datas):
            await sio.emit('data', {'sensor_id': idx, 'time': time(), 'data': data})
            await sio.sleep(0)

        model_result = inference(model, datas, scaler, threshold)

        await sio.emit('model', {'time': time(), 'result': model_result})
        await sio.sleep(0)


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

sio.start_background_task(loop)
