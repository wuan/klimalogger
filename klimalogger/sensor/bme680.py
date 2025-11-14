import adafruit_bme680
import busio

from .. import DataBuilder
from ..calc import PressureCalc, TemperatureCalc
from ..config import Config
from ..logger import create_logger
from ..measurement import Measurements
from . import BaseSensor

log = create_logger(__name__)


class BME680Sensor(BaseSensor):
    name: str = "BME680"
    priority: int = 1

    def __init__(
        self,
        i2c_bus: busio.I2C,
        address: int,
        config: Config,
        temperature_calc: TemperatureCalc,
        pressure_calc: PressureCalc,
    ):
        log.info("init()")
        self.temperature_calc = temperature_calc
        self.pressure_calc = pressure_calc
        self.elevation = int(config.elevation or 0)
        self.driver = adafruit_bme680.Adafruit_BME680_I2C(i2c_bus, address)
        self.driver.set_gas_heater(None, None)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        temperature = self.driver.temperature
        relative_humidity = self.driver.relative_humidity
        dew_point = self.temperature_calc.dew_point(temperature, relative_humidity)
        pressure = self.driver.pressure
        sea_level_pressure = self.pressure_calc.sea_level_pressure(
            pressure, temperature, self.elevation
        )

        data_builder.add(self.name, "temperature", "°C", round(temperature, 2))
        data_builder.add(
            self.name, "relative humidity", "%", round(relative_humidity, 2)
        )
        data_builder.add(
            self.name, "dew point", "°C", round(dew_point, 2), is_calculated=True
        )
        data_builder.add(self.name, "pressure", "hPa", round(pressure, 2))
        data_builder.add(
            self.name, "sea level pressure", "hPa", round(sea_level_pressure, 2)
        )

        measurements.temperature = temperature
        measurements.relative_humidity = relative_humidity
