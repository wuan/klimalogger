# -*- coding: utf8 -*-

from injector import singleton, inject

try:
    import configparser
except ImportError:
    import configparser as configparser

import board
import adafruit_bme680

@singleton
class Sensor:
    name = "BME680"

    @inject
    def __init__(self, config_parser: configparser.ConfigParser):
        self.elevation = int(config_parser.get('bme680_sensor', 'elevation'))
        i2c = board.I2C()
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

    def measure(self, data_builder):
        temperature = self.sensor.temperature
        relative_humidity = self.sensor.relative_humidity
        pressure = self.sensor.pressure
        voc_gas = self.sensor.gas

        data_builder.add(self.name, "temperature", "°C", temperature)
        data_builder.add(self.name, "relative humidity", "%", relative_humidity)
        data_builder.add(self.name, "pressure", "Pa", pressure)
        data_builder.add(self.name, "voc gas", "Ohm", voc_gas)