from typing import List
from fastapi import FastAPI
import model
from pydantic import BaseModel
import pandas as pd
import configparser
import os

config = configparser.ConfigParser()
config.read('../config.ini')
print('config loaded')

modelPath = config['model']['modelPath']
motorPath = os.path.join(modelPath, config['model']['motorModelFileName'])
pumpPath = os.path.join(modelPath, config['model']['pumpmodelfilename'])

print('motor model path = ' + motorPath)
print('pump model path = ' + pumpPath)

app = FastAPI()
motor = model.Model.load_model(motorPath)
pump = model.Model.load_model(pumpPath)
print('model loaded')


class Data(BaseModel):
    array: List[float]


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
