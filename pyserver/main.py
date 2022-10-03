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
    value: str


class Model(BaseModel):
    sensor_data: List[float]
    model_res: List[int]


device_name, device_channel_name, sampling_rate, samples_per_channel, type = config.load(
    'config.ini')

sensor = Sensor.of(device_name, device_channel_name,
                   sampling_rate, samples_per_channel * 2, type)

sio = socketio.AsyncServer()

# 모델 로딩
mae = tf.keras.models.load_model('model/')


async def loop():
    datas = await sensor.read(samples_per_channel)
    now = datetime.now()
    await sio.emit('data', {'sensor_id': 0, 'time': now, 'data': datas})
    # TODO request to model and get res
    await sio.emit('model', {'time': now, 'result': datas})

asyncio.run(loop())
