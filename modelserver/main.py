from fastapi import FastAPI
import model
import pandas as pd
import numpy as np

app = FastAPI()
motor = model.Model.load_model('motor_tmp.pkl')
pump = model.Model.load_model('pump_tmp.pkl')

#만개 단위로 송수신
@app.get("/model/pump")
def detect_pump():
    arr = np.random.randn(100);
    df = pd.DataFrame(arr).astype('float')
    return {"res": motor.predict(df)}

@app.get("/model/motor")
def detect_pump():
    arr = np.random.randn(100);
    df = pd.DataFrame(arr).astype('float')
    return {"res": pump.predict(df)}