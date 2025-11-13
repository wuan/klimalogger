import time

try:
    from collections.abc import Callable
except ImportError:
    pass

import busio

from klimalogger import DataBuilder

from .calc import PressureCalc, TemperatureCalc
from .config import Config
from .logger import create_logger
from .measurement import Measurements
from .sensor import BaseSensor
from .sensor.bh1750 import BH1750Sensor
from .sensor.bme680 import BME680Sensor
from .sensor.bmp3xx import BMP3xxSensor
from .sensor.dps310 import DPS310Sensor
from .sensor.mmc56x3 import MMC56x3Sensor
from .sensor.pm25 import PM25Sensor
from .sensor.scd4x import SCD4xSensor
from .sensor.sgp40 import SGP40Sensor
from .sensor.sht4x import SHT4xSensor
from .sensor.tsl2591 import TSL2591Sensor
from .sensor.veml7700 import VEML7700Sensor

log = create_logger(__name__)


def scan(i2c_bus: busio.I2C):
    lock_attempts = 0
    while not i2c_bus.try_lock():
        lock_attempts += 1

    if lock_attempts > 1:
        log.debug(f"scan() attempts: {lock_attempts}")

    devices = []
    iterations = 0
    for _ in range(20):
        devices = i2c_bus.scan()
        if devices:
            break
        time.sleep(0.2)
        iterations += 1
    log.info(f"Found {len(devices)} devices after {iterations} iterations.")

    i2c_bus.unlock()

    return devices


class Sensors:
    sensor_map: dict[str, Callable] = {
        SCD4xSensor.name: lambda i2c_bus, address, _: SCD4xSensor(i2c_bus, address),
        SGP40Sensor.name: lambda i2c_bus, address, _: SGP40Sensor(i2c_bus, address),
        SHT4xSensor.name: lambda i2c_bus, address, _: SHT4xSensor(
            i2c_bus, address, TemperatureCalc()
        ),
        BMP3xxSensor.name: lambda i2c_bus, address, config: BMP3xxSensor(
            i2c_bus, address, config, PressureCalc()
        ),
        BME680Sensor.name: lambda i2c_bus, address, config: BME680Sensor(
            i2c_bus, address, config, TemperatureCalc(), PressureCalc()
        ),
        MMC56x3Sensor.name: lambda i2c_bus, address, _: MMC56x3Sensor(i2c_bus, address),
        VEML7700Sensor.name: lambda i2c_bus, address, _: VEML7700Sensor(
            i2c_bus, address
        ),
        BH1750Sensor.name: lambda i2c_bus, _1, _2: BH1750Sensor(i2c_bus),
        PM25Sensor.name: lambda i2c_bus, _1, _2: PM25Sensor(i2c_bus),
        TSL2591Sensor.name: lambda i2c_bus, _1, _2: TSL2591Sensor(i2c_bus),
        DPS310Sensor.name: lambda i2c_bus, _, config: DPS310Sensor(
            i2c_bus, config, PressureCalc()
        ),
    }

    def __init__(self, config: Config, i2c_bus: busio.I2C):
        self.config = config
        self.i2c_bus = i2c_bus
        self.active_sensors: list[BaseSensor] = []

        self.device_map: dict[int, str] = {
            16: VEML7700Sensor.name,
            18: PM25Sensor.name,
            35: BH1750Sensor.name,
            41: TSL2591Sensor.name,
            48: MMC56x3Sensor.name,
            68: SHT4xSensor.name,
            89: SGP40Sensor.name,
            98: SCD4xSensor.name,
            119: BME680Sensor.name,
        }
        device_map = config.device_map
        if device_map:
            self.device_map.update(device_map)
        self.address_map: dict[str, int] = {
            sensor_name: address for address, sensor_name in self.device_map.items()
        }

        self.scan_devices()

    def scan_devices(self):
        active_sensors = {sensor.name for sensor in self.active_sensors}

        device_addresses = (
            scan(self.i2c_bus) if not self.config.sensors else self.config.sensors
        )

        sensors_found = {
            self.device_map[device_address]
            for device_address in device_addresses
            if device_address in self.device_map
        }
        unknown_sensors_found = {
            str(device_address)
            for device_address in device_addresses
            if device_address not in self.device_map
        }
        if unknown_sensors_found:
            log.warning(
                f"Could not find sensors for addresses: {', '.join(unknown_sensors_found)}"
            )

        if active_sensors != sensors_found:

            sensors = [
                sensor for sensor in self.active_sensors if sensor.name in sensors_found
            ]
            for sensor_name in sensors_found.difference(active_sensors):
                if sensor_name in self.sensor_map:
                    sensor = self.sensor_map[sensor_name]
                    address = self.address_map[sensor_name]
                    sensors.append(sensor(self.i2c_bus, address, self.config))

            sensors.sort(key=lambda sensor: sensor.priority)

            log.info("updated sensors:")
            for sensor in sensors:
                log.info(f"  {sensor.name} {sensor.priority}")

            self.active_sensors = sensors

    def measure(self, data_builder=None) -> DataBuilder:
        if data_builder is None:
            data_builder = DataBuilder()
        measurements = Measurements()

        for sensor in self.active_sensors:
            try:
                start_time = time.monotonic_ns()
                sensor.measure(data_builder, measurements)
                end_time = time.monotonic_ns()
                data_builder.add(
                    sensor.name, "time", "ms", (end_time - start_time) / 1e6
                )
            except OSError:
                pass

        return data_builder
