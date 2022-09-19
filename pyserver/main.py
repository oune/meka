from typing import List
from pydantic import BaseModel
from sensor import Sensor
from fastapi import FastAPI
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


mae = tf.keras.models.load_model('model/model_loss_test.h5')
mse = tf.keras.models.load_model('model/model_loss_test.h5')


async def loop():
    datas = await sensor.read()
    sio.emit('data', {'data': datas})
    # TODO request to model
    # TODO emit 'model_res'

asyncio.run(loop())
