import adafruit_sht4x
import busio

from .. import DataBuilder
from ..calc import TemperatureCalc
from ..logger import create_logger
from ..measurement import Measurements
from . import BaseSensor

log = create_logger(__name__)


class SHT4xSensor(BaseSensor):
    name: str = "SHT4x"
    priority: int = 1

    def __init__(
        self, i2c_bus: busio.I2C, address: int, temperature_calc: TemperatureCalc
    ):
        log.info("init")
        self.temperature_calc = temperature_calc

        self.driver = adafruit_sht4x.SHT4x(i2c_bus, address)

        # self.sensor.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
        # Can also set the mode to enable heater
        # sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        (temperature, relative_humidity) = self.driver.measurements

        if temperature > -40.0:
            try:
                dew_point = self.temperature_calc.dew_point(
                    temperature, relative_humidity
                )
                dew_point = round(dew_point, 2)
            except ValueError:
                log.warning(
                    f"measure calc_dew_point({temperature}, {relative_humidity}) failed"
                )
                dew_point = None

            temperature = round(temperature, 2)
            relative_humidity = round(relative_humidity, 2)
        else:
            temperature = None
            relative_humidity = None
            dew_point = None

        if (
            temperature
            and relative_humidity
            and -30 < temperature < 80
            and 5 < relative_humidity <= 100
        ):
            measurements.temperature = temperature
            measurements.relative_humidity = relative_humidity

            data_builder.add(self.name, "temperature", "°C", temperature)
            if dew_point:
                data_builder.add(self.name, "dew point", "°C", dew_point, True)
            data_builder.add(self.name, "relative humidity", "%", relative_humidity)
