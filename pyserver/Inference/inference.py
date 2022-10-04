import numpy as np
import tensorflow as tf
import joblib
from ae_LSTM import autoencoder_model


model_path = r'../models/model.h5'  # model.h5 path
scaler_path = r'../models/pipeline.pkl'  # StandardScaler -> pipeline.pkl path
input_shape = (1, 4)
threshold = 0.000833  # 유동적으로 지정

scaler = joblib.load(scaler_path)  # load pipeline.pkl
model = autoencoder_model(input_shape)  # 여기 부분 이상함
model = tf.keras.models.load_model(model_path)  # load model.h5


def inference(model, data, scaler, threshold):
    data_0, data_1, data_2, data_3 = data

    data_0 = scaler.transform(np.mean(np.abs(data_0), axis=0))
    data_1 = scaler.transform(np.mean(np.abs(data_1), axis=0))
    data_2 = scaler.transform(np.mean(np.abs(data_2), axis=0))
    data_3 = scaler.transform(np.mean(np.abs(data_3), axis=0))

    test_data = np.stack([data_0, data_1, data_2, data_3])
    test_data = test_data.reshape(1, 1, 4)

    output = model(test_data).numpy().reshape(1, 4)

    output_mse = np.mean(np.power(test_data.reshape(1, 4) - output, 2), axis=1)

    return (output_mse > threshold).item()
