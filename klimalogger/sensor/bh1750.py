import adafruit_bh1750
import busio

from ..data_builder import DataBuilder
from ..measurement import Measurements
from . import BaseSensor


class BH1750Sensor(BaseSensor):
    name: str = "BH1750"
    priority: int = 1

    def __init__(self, i2c_bus: busio.I2C):
        self.driver = adafruit_bh1750.BH1750(i2c_bus)

    def __del__(self):
        self.driver.stop_periodic_measurement()

    def measure(self, data_builder: DataBuilder, _: Measurements) -> None:
        light = self.driver.lux

        data_builder.add(self.name, "light", "Lux", float(light))
