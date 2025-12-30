from unittest.mock import patch

import pytest

from klimalogger.sensor.tsl2591 import TSL2591Sensor


@pytest.fixture
def sensor():
    with patch(
        "klimalogger.sensor.tsl2591.adafruit_tsl2591.TSL2591", autospec=True
    ) as mock_cls:
        yield mock_cls


@pytest.fixture
def uut(sensor, i2c_bus):
    return TSL2591Sensor(i2c_bus=i2c_bus)


def test_measure_adds_all_channels(uut, sensor, data_builder, measurements, tuv):
    sensor.return_value.lux = 12.34
    sensor.return_value.infrared = 101
    sensor.return_value.visible = 202
    sensor.return_value.full_spectrum = 303

    uut.measure(data_builder, measurements)

    t = tuv(data_builder.data)
    assert ("light", "lux", 12.34) in t
