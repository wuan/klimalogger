import logging

from injector import singleton, inject, Injector

import importlib

import configparser

from .data_builder import DataBuilder

log = logging.getLogger(__name__)

@singleton
class SensorFactory(object):
    @inject
    def __init__(self, configuration: configparser.ConfigParser, current_injector : Injector):
        self.sensors = [sensor.strip() for sensor in configuration.get('client', 'sensors').split(',')]
        self.current_injector = current_injector

    def measure(self, data_builder: DataBuilder):
        for sensor in self.sensors:
            try:
                module = importlib.import_module('klimalogger.sensor.' + sensor + '_sensor')
                log.info("sensor: %s, module: %s", sensor, module)
                sensor = self.current_injector.get(module.Sensor)
                sensor.measure(data_builder)
                del(sensor)
            except BaseException as e:
                log.error("measurement of sensor %s failed", sensor, e)

