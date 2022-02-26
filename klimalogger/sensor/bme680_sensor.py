# -*- coding: utf8 -*-

from injector import singleton, inject

from ..calc import PressureCalc, TemperatureCalc

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
    def __init__(self, config_parser: configparser.ConfigParser, temperature_calc: TemperatureCalc,
                 pressure_calc: PressureCalc):
        self.temperature_calc = temperature_calc
        self.pressure_calc = pressure_calc
        self.elevation = int(config_parser.get('bme680_sensor', 'elevation'))
        i2c = board.I2C()
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

    def measure(self, data_builder):
        temperature = self.sensor.temperature
        relative_humidity = self.sensor.relative_humidity
        dew_point = self.temperature_calc.dew_point(temperature, relative_humidity)
        pressure = self.sensor.pressure
        sea_level_pressure = self.pressure_calc.sea_level_pressure(pressure, temperature, self.elevation)
        voc_gas = self.sensor.gas

        data_builder.add(self.name, "temperature", "°C", round(temperature, 2))
        data_builder.add(self.name, "relative humidity", "%", round(relative_humidity, 2))
        data_builder.add(self.name, "dew point", "°C", round(dew_point, 2), is_calculated=True)
        data_builder.add(self.name, "pressure", "hPa", round(pressure, 2))
        data_builder.add(self.name, "sea level pressure", "hPa", round(sea_level_pressure, 2))
        data_builder.add(self.name, "voc gas", "Ohm", float(voc_gas))
