# -*- coding: utf8 -*-

from injector import singleton, inject

try:
    import configparser
except ImportError:
    import configparser as configparser

import board
import busio
import adafruit_sgp30


@singleton
class Sensor:
    name = "SGP30"

    @inject
    def __init__(self, config_parser: configparser.ConfigParser):
        i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.sensor = adafruit_sgp30.Adafruit_SGP30(i2c_bus)

    def measure(self, data_builder):
        eCO2, TVOC = self.sensor.iaq_measure()

        data_builder.add(self.name, "eCO2", "ppm", eCO2)
        data_builder.add(self.name, "TVOC", "ppb", TVOC)
