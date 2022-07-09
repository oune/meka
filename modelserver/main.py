from typing import List
from fastapi import FastAPI
import model
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()
motor = model.Model.load_model('../model/motor.pkl')
pump = model.Model.load_model('../model/pump.pkl')


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
