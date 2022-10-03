# -*- coding: utf8 -*-

import adafruit_sgp40
import board
import busio
from injector import singleton, inject

from klimalogger import DataBuilder
from klimalogger.measurement import Measurements


@singleton
class Sensor:
    name = "SGP40"
    priority = 3

    @inject
    def __init__(self, i2c_bus: busio.I2C):
        self.sensor = adafruit_sgp40.SGP40(i2c_bus)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        voc_index = None
        if measurements.temperature is not None and measurements.relative_humidity is not None:
            raw_gas = self.sensor.measure_raw(
                temperature=measurements.temperature, relative_humidity=measurements.relative_humidity
            )
            voc_index = self.sensor.measure_index(
                temperature=measurements.temperature, relative_humidity=measurements.relative_humidity)
        else:
            raw_gas = self.sensor.raw

        data_builder.add(self.name, "raw gas", "", float(raw_gas))
        if voc_index is not None:
            data_builder.add(self.name, "VOC index", "", float(voc_index))
