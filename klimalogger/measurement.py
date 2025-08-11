import configparser
import importlib
import inspect
import logging
import time
from dataclasses import dataclass
from typing import Optional

from lazy import lazy

from .calc import TemperatureCalc, PressureCalc
from .data_builder import DataBuilder
from .sensor import create_i2c_bus

log = logging.getLogger(__name__)


@dataclass
class Measurements:
    temperature: Optional[float] = None
    relative_humidity: Optional[float] = None


class MeasurementDispatcher:
    def __init__(self, configuration: configparser.ConfigParser, sensor_factory: "SensorFactory"):
        self.sensor_factory = sensor_factory
        self.sensor_names = [sensor.strip() for sensor in configuration.get('client', 'sensors').split(',') if
                             sensor.strip() != ""]

    def measure(self) -> DataBuilder:
        log.info("measure()")
        data_builder = DataBuilder()
        measurements = Measurements()
        for sensor in self.sensors:
            try:
                start_time = time.time()
                sensor.measure(data_builder, measurements)
                end_time = time.time()
                measurement_duration = round((end_time - start_time) * 1e3, 1)
                data_builder.add(sensor.name, "time", "ms", measurement_duration)
            except Exception:
                log.exception("measurement of sensor %s failed", sensor)

        return data_builder

    @lazy
    def sensors(self):
        log.info("sensors()")
        sensors = [self.sensor_factory.create_sensor(sensor_name) for sensor_name in self.sensor_names]
        return sorted(sensors, key=lambda entry: entry.priority)


class SensorFactory:

    def __init__(self, configuration: configparser.ConfigParser):
        self._config_parser = configuration
        self._i2c_bus = None
        self._temperature_calc = TemperatureCalc()
        self._pressure_calc = PressureCalc()

    def _deps(self):
        # Lazy create i2c bus
        if self._i2c_bus is None:
            try:
                self._i2c_bus = create_i2c_bus()
            except Exception:
                log.exception("Failed to create I2C bus")
                self._i2c_bus = None
        return {
            'i2c_bus': self._i2c_bus,
            'config_parser': self._config_parser,
            'temperature_calc': self._temperature_calc,
            'pressure_calc': self._pressure_calc,
        }

    def create_sensor(self, sensor_type: str):
        try:
            module = importlib.import_module('klimalogger.sensor.' + sensor_type + '_sensor')
            log.info("sensor: %s, module: %s", sensor_type, module)
            SensorCls = module.Sensor
            sig = inspect.signature(SensorCls.__init__)
            deps = self._deps()
            kwargs = {name: value for name, value in deps.items() if name in sig.parameters}
            return SensorCls(**kwargs)
        except Exception:
            log.exception("instatiation of sensor %s failed", sensor_type)
