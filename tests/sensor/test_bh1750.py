from unittest.mock import patch

import pytest

from klimalogger.sensor.bh1750 import BH1750Sensor


@pytest.fixture
def sensor():
    with patch(
        "klimalogger.sensor.bh1750.adafruit_bh1750.BH1750", autospec=True
    ) as mock_cls:
        yield mock_cls


@pytest.fixture
def uut(sensor, i2c_bus):
    return BH1750Sensor(i2c_bus=i2c_bus)


def test_measure_adds_light_value(uut, sensor, data_builder, measurements, tuv):
    sensor.return_value.lux = 321.987

    uut.measure(data_builder, measurements)

    assert ("light", "Lux", 321.987) in tuv(data_builder.data)
