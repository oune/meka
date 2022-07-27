from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

modelPath = config['model']['modelPath']
app = FastAPI()


class Data(BaseModel):
    array: List[float]


@app.get("/")
async def get_webpage():
    return ""


@app.post("/model/pump")
async def detect_pump(data: Data):
    return ""


@app.post("/model/motor")
async def detect_pump(data: Data):
    return ""


@app.get("/config")
async def get_config():
    return ""


@app.put("/config")
async def update_config(data):
    return ""
