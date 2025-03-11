import importlib
import logging
import time
from dataclasses import dataclass
from typing import Optional

from lazy import lazy

from .i2c import Sensors
from .data_builder import DataBuilder

log = logging.getLogger(__name__)


@dataclass
class Measurements:
    temperature: Optional[float] = None
    relative_humidity: Optional[float] = None


class MeasurementDispatcher:
    def __init__(self, sensors: Sensors):
        self.sensors = sensors

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

