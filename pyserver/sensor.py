import nidaqmx
import nidaqmx.system
from nidaqmx.constants import *


class Sensor:
    def __init__(self, device, rate, samples_per_channel):
        self.device = device
        self.task = nidaqmx.Task()
        self.task.timing.cfg_samp_clk_timing(rate=rate,
                                             active_edge=nidaqmx.constants.Edge.RISING,
                                             sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
                                             samps_per_chan=samples_per_channel)

    def add_vib_channel(self, channel: str):
        channel_name: str = self.device.name + "/" + channel
        self.task.ai_channels.add_ai_voltage_chan(channel_name)

    def add_temp_channel(self, channel: str):
        channel_name: str = self.device.name + "/" + channel
        self.task.ai_channels.add_ai_rtd_chan(channel_name, min_val=0.0, max_val=100.0, rtd_type=RTDType.PT_3750,
                                              resistance_config=ResistanceConfiguration.THREE_WIRE, current_excit_source=ExcitationSource.INTERNAL, current_excit_val=0.00100)

    async def read(self):
        return self.task.read(number_of_samples_per_channel=-1)
