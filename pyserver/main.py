from typing import List
from pydantic import BaseModel
from sensor import Sensor
from fastapi import FastAPI
from datetime import datetime
import pandas as pd
import tensorflow as tf
import socketio
import asyncio
import config


class Setting(BaseModel):
    sensor_id: int
    option: str
    data: str


class Model(BaseModel):
    sensor_id: int
    sensor_data: List[float]
    model_res: List[int]


device_name, device_channel_name, sampling_rate, samples_per_channel, type = config.load(
    'config.ini')

sensor = Sensor.of(device_name, device_channel_name,
                   sampling_rate, samples_per_channel, type)

sio = socketio.AsyncServer()
app = FastAPI()
app = socketio.WSGIApp(sio, app)

# change my setting by request


@app.put('setting')
def setting_change(_, data: Setting):
    print(data)
    pass


# 모델 로딩
mae = tf.keras.models.load_model('model/')


async def loop():
    datas = await sensor.read(68000)
    now = datetime.now()
    sio.emit('data', {'sensor_id': 0, 'time': now, 'data': datas})
    # TODO request to model and get res
    # TODO async await

    sio.emit('model', {'time': now, 'result': datas})

asyncio.run(loop())
