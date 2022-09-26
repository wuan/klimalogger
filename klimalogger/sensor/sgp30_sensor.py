# -*- coding: utf8 -*-
from typing import Any

from injector import singleton, inject

try:
    import configparser
except ImportError:
    import configparser as configparser

import board
import busio
from adafruit_sgp30 import Adafruit_SGP30, _SGP30_DEFAULT_I2C_ADDR, _SGP30_FEATURESETS
from adafruit_bus_device.i2c_device import I2CDevice


class UninitializedAdafruitSGP30(Adafruit_SGP30):

    def __init__(self, i2c: Any, address: Any = _SGP30_DEFAULT_I2C_ADDR):
        self._device = I2CDevice(i2c, address)

        # get unique serial, its 48 bits so we store in an array
        self.serial = self._i2c_read_words_from_cmd([0x36, 0x82], 0.01, 3)
        # get featureset
        featureset = self._i2c_read_words_from_cmd([0x20, 0x2F], 0.01, 1)
        if featureset[0] not in _SGP30_FEATURESETS:
            raise RuntimeError("SGP30 Not detected")


@singleton
class Sensor:
    name = "SGP30"

    @inject
    def __init__(self, config_parser: configparser.ConfigParser):
        self.baseline_eCO2 = int(config_parser.get('sgp30_sensor', 'baseline_eCO2'))
        self.baseline_TVOC = int(config_parser.get('sgp30_sensor', 'baseline_TVOC'))

        i2c_bus = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.sensor = UninitializedAdafruitSGP30(i2c_bus)

    def measure(self, data_builder):
        # self.sensor.set_iaq_baseline(self.baseline_eCO2, self.baseline_TVOC)
        eCO2, TVOC = self.sensor.iaq_measure()

        data_builder.add(self.name, "eCO2", "ppm", float(eCO2))
        data_builder.add(self.name, "TVOC", "ppb", float(TVOC))
