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
def get_webpage():
    return ""


@app.post("/model/pump")
def detect_pump(data: Data):
    return ""


@app.post("/model/motor")
def detect_pump(data: Data):
    return ""


@app.get("/config")
def get_config():
    return ""


@app.put("/config")
def update_config(data):
    return ""
