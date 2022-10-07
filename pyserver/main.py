from sensor import Sensor
from time import ctime, time
from Inference.inference import mse, model, threshold
from sys import exit

from uvicorn import Config, Server
import nidaqmx
import socketio
import config
import asyncio

device_name, device_channel_name, sampling_rate, samples_per_channel, modeltype, ip, port = config.load(
    f'config.ini')

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
task = sio.start_background_task(loop)
app = socketio.ASGIApp(sio)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    config = Config(app=app, host="127.0.0.1", port=8000, loop=loop)
    server = Server(config)
    loop.run_until_complete(server.serve())
    loop.run_until_complete(task)
