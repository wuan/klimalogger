import adafruit_sgp30
import busio

from klimalogger import Config, DataBuilder
from klimalogger.measurement import Measurements

from . import BaseSensor


class SGP30Sensor(BaseSensor):
    name = "SGP30"
    priority = 3

    def __init__(self, i2c_bus: busio.I2C, config: Config):
        self.baseline_eCO2 = config.baselines.get("eCO2")
        self.baseline_TVOC = config.baselines.get("TVOC")

        self.driver = adafruit_sgp30.Adafruit_SGP30(i2c_bus)

    def measure(self, data_builder: DataBuilder, _: Measurements) -> None:
        # self.sensor.set_iaq_baseline(self.baseline_eCO2, self.baseline_TVOC)
        carbon_dioxide_equivalent, total_volatile_organic_compounds = (
            self.driver.iaq_measure()
        )

        data_builder.add(self.name, "eCO2", "ppm", float(carbon_dioxide_equivalent))
        data_builder.add(
            self.name, "TVOC", "ppb", float(total_volatile_organic_compounds)
        )
