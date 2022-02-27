# -*- coding: utf8 -*-

from injector import singleton, inject

from ..calc import PressureCalc

try:
    import configparser
except ImportError:
    import configparser as configparser

import board
import adafruit_bmp3xx

@singleton
class Sensor:
    name = "BMP3xx"

    @inject
    def __init__(self, config_parser: configparser.ConfigParser, pressure_calc: PressureCalc):
        self.pressure_calc = pressure_calc
        self.elevation = int(config_parser.get('bmp3xx_sensor', 'elevation'))

        i2c = board.I2C()
        self.sensor = adafruit_bmp3xx.BMP3XX_I2C(i2c)

    def measure(self, data_builder):
        temperature = self.sensor.temperature
        pressure = self.sensor.pressure
        sea_level_pressure = self.pressure_calc.sea_level_pressure(pressure, temperature, self.elevation)

        data_builder.add(self.name, "pressure", "hPa", round(pressure,2))
        data_builder.add(self.name, "sea level pressure", "hPa", round(sea_level_pressure,2), is_calculated=True)