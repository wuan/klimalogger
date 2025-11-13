import adafruit_sgp40
import busio

from klimalogger import DataBuilder
from klimalogger.measurement import Measurements

from . import BaseSensor


class SGP40Sensor(BaseSensor):
    name: str = "SGP40"
    priority: int = 3

    def __init__(self, i2c_bus: busio.I2C, address: int):
        self.driver = adafruit_sgp40.SGP40(i2c_bus, address)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        if (
            measurements.temperature is not None
            and measurements.relative_humidity is not None
        ):
            data_builder.add(
                self.name,
                "VOC index",
                "",
                float(
                    self.driver.measure_index(
                        temperature=measurements.temperature,
                        relative_humidity=measurements.relative_humidity,
                    )
                ),
            )
        else:
            value = self.driver.raw
            data_builder.add(self.name, "raw gas", "", float(value))
