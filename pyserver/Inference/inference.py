import numpy as np
import tensorflow as tf
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = f'{BASE_DIR}/models/model.h5'  # model.h5 path
input_shape = (1, 4)
threshold = 0.000833  # 유동적으로 지정

model = tf.keras.models.load_model(model_path)  # load model.h5


def mse(model, data):
    data = np.array(data)

    data_0, data_1, data_2, data_3 = data

    data_0 = np.mean(np.abs(data_0), axis=0)
    data_1 = np.mean(np.abs(data_1), axis=0)
    data_2 = np.mean(np.abs(data_2), axis=0)
    data_3 = np.mean(np.abs(data_3), axis=0)

    test_data = np.stack([data_0, data_1, data_2, data_3])
    test_data = test_data.reshape(1, 1, 4)
    test_data = tf.convert_to_tensor(test_data)

    output = model(test_data).numpy().reshape(1, 4)
    output_mse = np.mean(
        np.power(test_data.numpy().reshape(1, 4) - output, 2), axis=1)

    return output_mse


def inference(model, data, threshold):
    output_mse = mse(model, data)

    return (output_mse > threshold).item()
