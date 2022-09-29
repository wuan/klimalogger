# -*- coding: utf8 -*-
import adafruit_sht4x
import board
from injector import singleton, inject

from .. import DataBuilder
from ..calc import TemperatureCalc
from ..measurement import Measurements


@singleton
class Sensor:
    name = "SHT4x"
    priority = 1

    @inject
    def __init__(self, temperature_calc: TemperatureCalc):
        self.temperature_calc = temperature_calc

        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_sht4x.SHT4x(i2c)

        self.sensor.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
        # Can also set the mode to enable heater
        # sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        (temperature, relative_humidity) = self.sensor.measurements

        if temperature > -40.0:
            try:
                dew_point = self.temperature_calc.dew_point(temperature, relative_humidity)
                dew_point = round(dew_point, 2)
            except ValueError:
                dew_point = None

            temperature = round(temperature, 2)
            relative_humidity = round(relative_humidity, 2)
        else:
            temperature = None
            relative_humidity = None
            dew_point = None

        if temperature and relative_humidity and dew_point and -30 < temperature < 80 and 5 < relative_humidity <= 100:
            measurements.temperature = temperature
            measurements.relative_humidity = relative_humidity

            data_builder.add(self.name, "temperature", "°C", temperature)
            if dew_point:
                data_builder.add(self.name, "dew point", "°C", dew_point, True)
            data_builder.add(self.name, "relative humidity", "%", relative_humidity)
