from typing import List
from pydantic import BaseModel
import pandas as pd
from PyQt5.QtWidgets import *

from sensor import Sensor
import config

device_name, device_channel_name, sampling_rate, samples_per_channel, type = config.load(
    'config.ini')

sensor = Sensor.of(device_name, device_channel_name,
                   sampling_rate, samples_per_channel, type)
