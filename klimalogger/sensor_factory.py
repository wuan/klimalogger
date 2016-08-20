from injector import singleton, inject, Injector

import importlib

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

@singleton
class SensorFactory(object):
    @inject(configuration=configparser.ConfigParser, current_injector=Injector)
    def __init__(self, configuration, current_injector):
        self.sensors = [sensor.strip() for sensor in configuration.get('client', 'sensors').split(',')]
        self.current_injector = current_injector

    def measure(self, data_builder):
        for sensor in self.sensors:
            module = importlib.import_module('klimalogger.sensor.' + sensor + '_sensor')
            print("module:", module)
            sensor = self.current_injector.get(module.Sensor)
            sensor.measure(data_builder)
