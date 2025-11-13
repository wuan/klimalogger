import busio
from adafruit_dps310.advanced import DPS310_Advanced as DPS310

from .. import Config, DataBuilder
from ..calc import PressureCalc
from ..measurement import Measurements
from . import BaseSensor

# from adafruit_dps310.basic import DPS310


class DPS310Sensor(BaseSensor):
    name: str = "DPS310"
    priority: int = 1

    def __init__(
        self,
        i2c_bus: busio.I2C,
        config: Config,
        pressure_calc: PressureCalc,
    ):
        self.elevation = config.elevation
        self.pressure_calc = pressure_calc

        self.driver = DPS310(i2c_bus)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        temperature = self.driver.temperature
        pressure = self.driver.pressure
        sea_level_pressure = (
            self.pressure_calc.sea_level_pressure(pressure, temperature, self.elevation)
            if pressure and self.elevation
            else None
        )

        data_builder.add(self.name, "temperature", "°C", round(temperature, 3))
        if pressure:
            data_builder.add(self.name, "pressure", "hPa", round(pressure, 3))
        if sea_level_pressure:
            data_builder.add(
                self.name, "sea level pressure", "hPa", round(sea_level_pressure, 3)
            )
