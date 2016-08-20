# -*- coding: utf8 -*-

from __future__ import print_function

from injector import singleton, inject

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from sht1x.Sht1x import Sht1x as SHT1x


@singleton
class Sensor(object):
    name = "SHT1x"

    @inject(config_parser=configparser.ConfigParser)
    def __init__(self, config_parser):
        data_pin = int(config_parser.get('sht1x_sensor', 'data_pin'))
        sck_pin = int(config_parser.get('sht1x_sensor', 'sck_pin'))

        self.sht1x = SHT1x(dataPin=data_pin, sckPin=sck_pin, gpioMode=SHT1x.GPIO_BOARD)

    def measure(self, data_builder):
        (temperature, humidity) = self.sht1x.read_temperature_C_and_humidity()

        if temperature > -40.0:
            print("valid values")
            dew_point = self.sht1x.calculate_dew_point(temperature, humidity)
            dew_point = round(dew_point, 2)

            temperature = round(temperature, 2)
            humidity = round(humidity, 2)
        else:
            temperature = None
            humidity = None
            dew_point = None

        data_builder.add(self.name, "temperature", "°C", temperature),
        data_builder.add(self.name, "dew point", "°C", dew_point, True),
        data_builder.add(self.name, "relative humidity", "%", humidity),
