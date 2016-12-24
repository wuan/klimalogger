from injector import singleton, inject, Injector

import importlib

import configparser

from .data_builder import DataBuilder


@singleton
class SensorFactory(object):
    @inject(configuration=configparser.ConfigParser, current_injector=Injector)
    def __init__(self, configuration, current_injector):
        self.sensors = [sensor.strip() for sensor in configuration.get('client', 'sensors').split(',')]
        self.current_injector = current_injector

    def measure(self, data_builder: DataBuilder):
        for sensor in self.sensors:
            module = importlib.import_module('klimalogger.sensor.' + sensor + '_sensor')
            print("module:", module)
            sensor = self.current_injector.get(module.Sensor)
            sensor.measure(data_builder)
