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
        now_time = ctime(time())

        for idx in range(0, len(datas)):
            await sio.emit('data', {'sensor_id': idx, 'time': now_time})
            await sio.sleep(1)

        output_mse = mse(model, datas)
        model_result = (output_mse > threshold).item()

        await sio.emit('model', {'time': now_time, 'mse': output_mse.item(),  'result': model_result})
        await sio.sleep(1)


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

sio.start_background_task(loop)
