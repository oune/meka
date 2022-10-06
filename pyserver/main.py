from typing import List
from pydantic import BaseModel
from sensor import Sensor
from time import ctime, time
from Inference.inference import inference, mse, model, scaler, threshold
from sys import exit

import nidaqmx
import socketio
import config

device_name, device_channel_name, sampling_rate, samples_per_channel, modeltype = config.load(
    'config.ini')

try:
    sensor = Sensor.of(device_name,
                       device_channel_name,
                       sampling_rate,
                       samples_per_channel * 2, modeltype)
except nidaqmx.errors.DaqError:
    print('잘못된 설정값이 입력 되었습니다. config.ini 파일을 올바르게 수정해 주세요.')
    exit()


async def loop():
    while True:
        datas = await sensor.read(samples_per_channel, 30.0)
        now_time = ctime(time())

        await sio.sleep(1)
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
