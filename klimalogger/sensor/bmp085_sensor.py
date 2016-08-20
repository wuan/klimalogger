# -*- coding: utf8 -*-

from __future__ import print_function

from injector import singleton, inject

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from Adafruit_BMP.BMP085 import BMP085


@singleton
class Sensor(object):
    name = "BMP085"

    @inject(config_parser=configparser.ConfigParser)
    def __init__(self, config_parser):
        self.elevation = int(config_parser.get('bmp085_sensor', 'elevation'))

        self.bmp085 = BMP085()

    def measure(self, data_builder):
        pressure = round(self.bmp085.read_sealevel_pressure(self.elevation) / 100, 2)

        data_builder.add("BMP085", "atmospheric pressure", "hPa", pressure)
