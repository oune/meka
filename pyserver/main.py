from typing import List
from pydantic import BaseModel
import pandas as pd
import sys
from PyQt5.QtWidgets import *

from sensor import Sensor
import config

device_name, device_channel_name, sampling_rate, samples_per_channel, type = config.load(
    'config.ini')

sensor = Sensor.of(device_name, device_channel_name,
                   sampling_rate, samples_per_channel, type)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('고장 진단 시스템')
        self.resize(400, 200)

        device_select = QComboBox(self)
        device_select.addItem('device a')
        device_select.addItem('device b')
        device_select.addItem('device c')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(device_select)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
