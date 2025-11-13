from unittest.mock import patch

import pytest

from klimalogger.sensor.veml7700 import VEML7700Sensor


@pytest.fixture
def sensor():
    with patch(
        "klimalogger.sensor.veml7700.adafruit_veml7700.VEML7700", autospec=True
    ) as mock_cls:
        yield mock_cls


@pytest.fixture
def uut(sensor, i2c_bus):
    # Provide an arbitrary I2C address
    return VEML7700Sensor(i2c_bus=i2c_bus, address=0x10)


def test_measure_adds_light_value(uut, sensor, data_builder, measurements, tuv):
    sensor.return_value.light = 123.456

    uut.measure(data_builder, measurements)

    assert ("light", "Lux", 123.456) in tuv(data_builder.data)
