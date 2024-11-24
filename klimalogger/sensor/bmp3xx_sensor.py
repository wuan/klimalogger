# -*- coding: utf8 -*-
import adafruit_bmp3xx
import busio
from setuptools.build_meta import prepare_metadata_for_build_editable

from .. import DataBuilder, Config
from ..measurements import Measurements
from ..calc.pressure import sea_level_pressure


class BMP3xxSensor:
    name = "BMP3xx"
    priority = 2

    def __init__(self, i2c_bus: busio.I2C, config: Config):
        self.elevation = config.elevation

        self.driver = adafruit_bmp3xx.BMP3XX_I2C(i2c_bus)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        temperature = self.driver.temperature
        pressure = self.driver.pressure
        sea_level_pressure = sea_level_pressure(pressure, temperature, self.elevation)

        data_builder.add(self.name, "pressure", "hPa", round(pressure, 2))
        data_builder.add(self.name, "sea level pressure", "hPa", round(sea_level_pressure, 2), is_calculated=True)
