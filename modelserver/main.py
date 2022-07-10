from typing import List
from fastapi import FastAPI
import model
from pydantic import BaseModel
import pandas as pd
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

modelPath = config['model']['modelPath']
motorPath = os.path.join(modelPath, config['model']['motorModelFileName'])
pumpPath = os.path.join(modelPath, config['model']['pumpmodelfilename'])

app = FastAPI()
motor = model.Model.load_model(motorPath)
pump = model.Model.load_model(pumpPath)


class Data(BaseModel):
    array: List[float]


# 만개 단위로 송수신
@app.post("/model/pump")
def detect_pump(data: Data):
    df = pd.DataFrame(data.array).astype('float')
    a, b = motor.predict(df)
    return {"predicted": a.tolist(), "score": b.tolist()}


@app.post("/model/motor")
def detect_pump(data: Data):
    df = pd.DataFrame(data.array).astype('float')
    a, b = pump.predict(df)
    return {"predicted": a.tolist(), "score": b.tolist()}
