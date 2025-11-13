import math

import adafruit_mmc56x3
import busio

from ..data_builder import DataBuilder
from ..measurement import Measurements
from . import BaseSensor


class MMC56x3Sensor(BaseSensor):
    name: str = "MMC56x3"
    priority: int = 1

    def __init__(self, i2c_bus: busio.I2C, address: int):
        self.driver = adafruit_mmc56x3.MMC5603(i2c_bus, address)
        # self.driver.data_rate = 10  # in Hz, from 1-255 or 1000
        # self.driver.continuous_mode = True

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        mag_x, mag_y, mag_z = self.driver.magnetic

        data_builder.add(self.name, "magX", "uT", float(mag_x))
        data_builder.add(self.name, "magY", "uT", float(mag_y))
        data_builder.add(self.name, "magZ", "uT", float(mag_z))

        mag = math.sqrt(mag_x**2 + mag_y**2 + mag_z**2)
        data_builder.add(self.name, "mag", "uT", float(mag), is_calculated=True)
