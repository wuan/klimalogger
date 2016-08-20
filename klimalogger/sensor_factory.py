from injector import singleton, inject, Injector

import importlib

from . import config


@singleton
class SensorFactory(object):
    @inject(configuration=config.Config, current_injector=Injector)
    def __init__(self, configuration, current_injector):
        self.sensors = [sensor.trim() for sensor in configuration.get('client', 'sensors').split(',')]
        self.current_injector = current_injector

    def measure(self, data_builder):
        for sensor in self.sensors:
            importlib.import_module('klimalogger.sensor.' + sensor + '.Sensor')
            sensor = self.current_injector.get(Sensor)
            sensor.measure(data_builder)
