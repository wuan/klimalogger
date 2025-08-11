# -*- coding: utf8 -*-
import busio

from .. import DataBuilder
from ..calc import PressureCalc
from ..measurement import Measurements

try:
    import configparser
except ImportError:
    import configparser as configparser

import adafruit_bmp3xx


class Sensor:
    name = "BMP3xx"
    priority = 2

    def __init__(self, i2c_bus: busio.I2C, config_parser: configparser.ConfigParser, pressure_calc: PressureCalc):
        self.pressure_calc = pressure_calc
        self.elevation = int(config_parser.get('bmp3xx_sensor', 'elevation'))

        self.driver = adafruit_bmp3xx.BMP3XX_I2C(i2c_bus)

    def measure(self, data_builder: DataBuilder, _: Measurements) -> None:
        temperature = self.driver.temperature
        pressure = self.driver.pressure
        sea_level_pressure = self.pressure_calc.sea_level_pressure(pressure, temperature, self.elevation)

        data_builder.add(self.name, "pressure", "hPa", round(pressure, 2))
        data_builder.add(self.name, "sea level pressure", "hPa", round(sea_level_pressure, 2), is_calculated=True)
