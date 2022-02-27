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
        self.baseline_eCO2 = int(config_parser.get('sgp30_sensor', 'baseline_eCO2'))
        self.baseline_TVOC = int(config_parser.get('sgp30_sensor', 'baseline_TVOC'))

        i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.sensor = adafruit_sgp30.Adafruit_SGP30(i2c_bus)

    def measure(self, data_builder):
        self.sensor.set_iaq_baseline(self.baseline_eCO2, self.baseline_TVOC)
        eCO2, TVOC = self.sensor.iaq_measure()

        data_builder.add(self.name, "eCO2", "ppm", float(eCO2))
        data_builder.add(self.name, "TVOC", "ppb", float(TVOC))
