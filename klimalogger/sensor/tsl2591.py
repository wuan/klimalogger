import adafruit_tsl2591
import busio

from .. import DataBuilder
from ..measurement import Measurements
from . import BaseSensor


class TSL2591Sensor(BaseSensor):
    name: str = "TSL2591"
    priority: int = 1

    def __init__(self, i2c_bus: busio.I2C):
        self.driver = adafruit_tsl2591.TSL2591(i2c_bus)

        # You can optionally change the gain and integration time:
        # self.driver.gain = adafruit_tsl2591.GAIN_LOW (1x gain)
        # self.driver.gain = adafruit_tsl2591.GAIN_MED (25x gain, the default)
        # self.driver.gain = adafruit_tsl2591.GAIN_HIGH (428x gain)
        # self.driver.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
        # self.driver.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS (100ms, default)
        # self.driver.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS (200ms)
        # self.driver.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
        # self.driver.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
        # self.driver.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
        # self.driver.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        lux = self.driver.lux
        data_builder.add(self.name, "light", "lux", lux)

        infrared = self.driver.infrared
        data_builder.add(self.name, "light_raw_infrared", "", infrared)

        visible = self.driver.visible
        data_builder.add(self.name, "light_raw_visible", "", visible)

        full_spectrum = self.driver.full_spectrum
        data_builder.add(self.name, "light_raw_full_spectrum", "", full_spectrum)
