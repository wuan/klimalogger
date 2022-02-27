# -*- coding: utf8 -*-

from injector import singleton, inject

try:
    import configparser
except ImportError:
    import configparser as configparser

from sht1x.Sht1x import Sht1x as SHT1x


@singleton
class Sensor:
    name = "SHT1x"

    @inject
    def __init__(self, config_parser: configparser.ConfigParser):
        data_pin = int(config_parser.get('sht1x_sensor', 'data_pin'))
        sck_pin = int(config_parser.get('sht1x_sensor', 'sck_pin'))

        self.sht1x = SHT1x(dataPin=data_pin, sckPin=sck_pin, gpioMode=SHT1x.GPIO_BCM)

    def measure(self, data_builder):
        (temperature, humidity) = self.sht1x.read_temperature_C_and_humidity()

        if temperature > -40.0:
            try:
                dew_point = self.sht1x.calculate_dew_point(temperature, humidity)
                dew_point = round(dew_point, 2)
            except ValueError:
                dew_point = None

            temperature = round(temperature, 2)
            humidity = round(humidity, 2)
        else:
            temperature = None
            humidity = None
            dew_point = None

        if temperature and humidity and dew_point and -30 < temperature < 80 and 5 < humidity <= 100:
            data_builder.add(self.name, "temperature", "°C", temperature)
            if dew_point:
                data_builder.add(self.name, "dew point", "°C", dew_point, True)
            data_builder.add(self.name, "relative humidity", "%", humidity)
