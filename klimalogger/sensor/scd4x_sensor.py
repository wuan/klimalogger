# -*- coding: utf8 -*-

import time

import adafruit_scd4x
import board
import busio
from injector import singleton, inject

from klimalogger import DataBuilder
from klimalogger.measurement import Measurements


@singleton
class Sensor:
    name = "SCD4x"
    priority = 3

    @inject
    def __init__(self):
        i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.sensor = adafruit_scd4x.SCD4X(i2c_bus)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        self.sensor.start_periodic_measurement()

        while True:
            if self.sensor.data_ready:
                CO2 = self.sensor.CO2
                break
            time.sleep(1)

        self.sensor.stop_periodic_measurement()

        data_builder.add(self.name, "CO2", "", float(CO2))
