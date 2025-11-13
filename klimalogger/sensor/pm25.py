import busio
from adafruit_pm25.i2c import PM25_I2C

from .. import DataBuilder
from ..measurement import Measurements
from . import BaseSensor


class PM25Sensor(BaseSensor):
    name: str = "PM25"
    priority: int = 1

    def __init__(self, i2c_bus: busio.I2C):
        reset_pin = None
        self.driver = PM25_I2C(i2c_bus, reset_pin)

    def measure(self, data_builder: DataBuilder, measurements: Measurements) -> None:
        try:
            aqdata = self.driver.read()
            # print(aqdata)
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            return

        for size in [
            "03",
            "05",
            "10",
            "25",
            "50",
            "100",
        ]:
            particles = aqdata.get(f"particles {size}um")
            if particles is not None:
                data_builder.add(self.name, f"particles_{size}", "#", particles)
            # environmental = aqdata.get(f"pm{size} env")
            standard = aqdata.get(f"pm{size} standard")
            if standard is not None:
                data_builder.add(self.name, f"part_con_{size}", "ug/m^3", standard)
