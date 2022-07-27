from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from sensor import Sensor
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

modelPath = config['model']['modelPath']
app = FastAPI()


class Data(BaseModel):
    array: List[float]


sensor = Sensor.vib("cDAQ1Mod1", "ai0:3", 51200, 51200)


async def detect_pump(data: Data):
    return ""


async def detect_pump(data: Data):
    return ""


@app.get("/")
async def get_webpage():
    return ""


@app.get("/config")
async def get_config():
    return ""


@app.put("/config")
async def update_config(data):
    return ""
