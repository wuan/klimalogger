import time

import adafruit_scd4x
import busio

from klimalogger import DataBuilder
from klimalogger.measurement import Measurements

from . import BaseSensor


class SCD4xSensor(BaseSensor):
    name: str = "SCD4x"
    priority: int = 3

    def __init__(self, i2c_bus: busio.I2C, address: int):
        self.driver = adafruit_scd4x.SCD4X(i2c_bus, address)
        self.driver.start_periodic_measurement()

    def __del__(self):
        self.driver.stop_periodic_measurement()

    def measure(self, data_builder: DataBuilder, _: Measurements) -> None:

        while True:
            CO2 = self.driver.CO2

            if CO2 is not None:
                break

            time.sleep(1)

        data_builder.add(self.name, "CO2", "ppm", float(CO2))
