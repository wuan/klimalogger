import math
from unittest.mock import patch

import pytest

from klimalogger.sensor.mmc56x3 import MMC56x3Sensor


@pytest.fixture
def sensor():
    with patch(
        "klimalogger.sensor.mmc56x3.adafruit_mmc56x3.MMC5603", autospec=True
    ) as mock_cls:
        yield mock_cls


@pytest.fixture
def uut(sensor, i2c_bus):
    return MMC56x3Sensor(i2c_bus=i2c_bus, address=0x30)


def test_measure_adds_vector_and_magnitude(uut, sensor, data_builder, measurements):
    mag = (1.5, -2.0, 3.0)
    sensor.return_value.magnetic = mag

    uut.measure(data_builder, measurements)

    # Expect X/Y/Z components
    records = data_builder.data

    def find(type_):
        return next(e for e in records if e["tags"]["type"] == type_)

    assert find("magX")["fields"]["value"] == float(mag[0])
    assert find("magY")["fields"]["value"] == float(mag[1])
    assert find("magZ")["fields"]["value"] == float(mag[2])

    # Magnitude with calculated flag
    mag_expected = math.sqrt(sum(v * v for v in mag))
    e = find("mag")
    assert e["fields"]["value"] == float(mag_expected)
    assert e["tags"]["unit"] == "uT"
    assert e["tags"]["calculated"] is True
