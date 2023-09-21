# -*- coding: utf8 -*-
import logging

import busio
from injector import singleton, inject

from .. import DataBuilder
from ..calc import PressureCalc, TemperatureCalc
from ..measurement import Measurements

try:
    import configparser
except ImportError:
    import configparser as configparser

import adafruit_bme680

log = logging.getLogger(__name__)


@singleton
class Sensor:
    name = "BME680"
    priority = 1

    @inject
    def __init__(self, i2c_bus: busio.I2C, config_parser: configparser.ConfigParser, temperature_calc: TemperatureCalc,
                 pressure_calc: PressureCalc):
        log.info("init()")
        self.temperature_calc = temperature_calc
        self.pressure_calc = pressure_calc
        self.elevation = int(config_parser.get('bme680_sensor', 'elevation'))
        self.driver = adafruit_bme680.Adafruit_BME680_I2C(i2c_bus)
        self.driver.set_gas_heater(None, None)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        temperature = self.driver.temperature
        relative_humidity = self.driver.relative_humidity
        dew_point = self.temperature_calc.dew_point(temperature, relative_humidity)
        pressure = self.driver.pressure
        sea_level_pressure = self.pressure_calc.sea_level_pressure(pressure, temperature, self.elevation)
        voc_gas = self.driver.gas

        data_builder.add(self.name, "temperature", "°C", round(temperature, 2))
        data_builder.add(self.name, "relative humidity", "%", round(relative_humidity, 2))
        data_builder.add(self.name, "dew point", "°C", round(dew_point, 2), is_calculated=True)
        data_builder.add(self.name, "pressure", "hPa", round(pressure, 2))
        data_builder.add(self.name, "sea level pressure", "hPa", round(sea_level_pressure, 2))
        data_builder.add(self.name, "voc gas", "Ohm", float(voc_gas))

        measurements.temperature = temperature
        measurements.relative_humidity = relative_humidity
