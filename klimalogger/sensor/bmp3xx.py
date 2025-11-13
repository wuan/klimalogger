import adafruit_bmp3xx
import busio

from .. import DataBuilder
from ..calc import PressureCalc
from ..config import Config
from ..measurement import Measurements
from . import BaseSensor


class BMP3xxSensor(BaseSensor):
    name: str = "BMP3xx"
    priority: int = 2

    def __init__(
        self,
        i2c_bus: busio.I2C,
        address: int,
        config: Config,
        pressure_calc: PressureCalc,
    ):
        self.pressure_calc = pressure_calc
        self.elevation = int(config.elevation or 0)

        self.driver = adafruit_bmp3xx.BMP3XX_I2C(i2c_bus, address)

    def measure(self, data_builder: DataBuilder, _: Measurements) -> None:
        temperature = self.driver.temperature
        pressure = self.driver.pressure
        sea_level_pressure = self.pressure_calc.sea_level_pressure(
            pressure, temperature, self.elevation
        )

        data_builder.add(self.name, "pressure", "hPa", round(pressure, 2))
        data_builder.add(
            self.name,
            "sea level pressure",
            "hPa",
            round(sea_level_pressure, 2),
            is_calculated=True,
        )
