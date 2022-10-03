import configparser
import importlib
import logging
from dataclasses import dataclass
from typing import Optional

from injector import singleton, inject, Injector
from lazy import lazy

from .data_builder import DataBuilderFactory, DataBuilder

log = logging.getLogger(__name__)


@dataclass
class Measurements:
    temperature: Optional[float] = None
    relative_humidity: Optional[float] = None


@singleton
class MeasurementDispatcher:
    @inject
    def __init__(self, configuration: configparser.ConfigParser, sensor_factory: "SensorFactory",
                 data_builder_factory: DataBuilderFactory):
        self.sensor_factory = sensor_factory
        self.data_builder_factory = data_builder_factory
        self.sensor_names = [sensor.strip() for sensor in configuration.get('client', 'sensors').split(',')]

    def measure(self) -> DataBuilder:
        log.info("measure()")
        data_builder = self.data_builder_factory.get()
        measurements = Measurements()
        for sensor in self.sensors:
            try:
                sensor.measure(data_builder, measurements)
            except BaseException as e:
                log.error("measurement of sensor %s failed", sensor, e)

        return data_builder

    @lazy
    def sensors(self):
        log.info("sensors()")
        sensors = [self.sensor_factory.create_sensor(sensor_name) for sensor_name in self.sensor_names]
        return sorted(sensors, key=lambda entry: entry.priority)


@singleton
class SensorFactory:

    @inject
    def __init__(self, current_injector: Injector):
        self.injector = current_injector

    def create_sensor(self, sensor_type: str):
        try:
            module = importlib.import_module('klimalogger.sensor.' + sensor_type + '_sensor')
            log.info("sensor: %s, module: %s", sensor_type, module)
            return self.injector.get(module.Sensor)
        except BaseException as e:
            log.error("instatiation of sensor %s failed", sensor_type, e)
