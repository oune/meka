from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from sensor import Sensor
import config

device_name, device_channel_name, sampling_rate, samples_per_channel, type = config.load(
    'config.ini')

sensor = Sensor.of(device_name, device_channel_name,
                   sampling_rate, samples_per_channel, type)


async def detect_pump(data: List[float]):
    return ""


async def detect_pump(data: List[float]):
    return ""

app = FastAPI()


@app.get("/")
async def get_webpage():
    return ""


@app.get("/config")
async def get_config():
    return ""


@app.put("/config")
async def update_config(data):
    return ""
