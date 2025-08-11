# -*- coding: utf8 -*-

from klimalogger import DataBuilder
from klimalogger.measurement import Measurements

try:
    import configparser
except ImportError:
    import configparser as configparser

from Adafruit_BMP.BMP085 import BMP085


class Sensor:
    name = "BMP085"
    priority = 2

    def __init__(self, config_parser: configparser.ConfigParser):
        self.elevation = int(config_parser.get('bmp085_sensor', 'elevation'))

        self.driver = BMP085()

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        pressure = round(self.driver.read_sealevel_pressure(self.elevation) / 100, 2)

        data_builder.add("BMP085", "sea level pressure", "hPa", pressure)
