from typing import List
from pydantic import BaseModel
from sensor import Sensor
from time import ctime, time
from Inference.inference import inference, mse, model, scaler, threshold

import socketio
import config

device_name, device_channel_name, sampling_rate, samples_per_channel, modeltype = config.load(
    'config.ini')

sensor = Sensor.of(device_name,
                   device_channel_name,
                   sampling_rate,
                   samples_per_channel * 2, modeltype)


async def loop():
    while True:
        datas = await sensor.read(samples_per_channel, 30.0)

        for idx in range(datas):
            await sio.emit('data', {'sensor_id': idx, 'time': time()})
            await sio.sleep(0)

        output_mse = mse(model, datas, threshold)
        model_result = (output_mse > threshold).item()

        await sio.emit('model', {'time': time(), 'result': model_result})
        await sio.sleep(0)


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

sio.start_background_task(loop)
