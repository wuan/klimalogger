import adafruit_veml7700
import busio

from ..data_builder import DataBuilder
from ..measurement import Measurements
from . import BaseSensor


class VEML7700Sensor(BaseSensor):
    name: str = "VEML7700"
    priority: int = 1

    def __init__(self, i2c_bus: busio.I2C, address: int):
        self.driver = adafruit_veml7700.VEML7700(i2c_bus, address)
        self.driver.data_rate = 10  # in Hz, from 1-255 or 1000
        self.driver.continuous_mode = True

    def __del__(self):
        self.driver.stop_periodic_measurement()

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        light = self.driver.light

        data_builder.add(self.name, "light", "Lux", float(light))
