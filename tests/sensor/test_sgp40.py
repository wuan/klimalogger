import sys
import types
from unittest import mock

import pytest
from mock import patch

from klimalogger.data_builder import DataBuilder
from klimalogger.measurement import Measurements
from sensor.sgp40_sensor import Sensor


@pytest.fixture
def sensor():
    with patch('sensor.sgp40_sensor.adafruit_sgp40', autospec=True) as mock:
        yield mock

@pytest.fixture
def uut(sensor, i2c_bus):
    return Sensor(i2c_bus=i2c_bus)

@pytest.fixture
def data_builder():
    return DataBuilder()

def test_index(uut, sensor, data_builder):
    sensor.SGP40.return_value.measure_index.return_value = 12.34

    uut.measure(data_builder, Measurements(20, 80))

    assert len(data_builder.data) == 1
    data = data_builder.data[0]
    assert data["measurement"] == "data"
    assert "value" in data["fields"]
    assert data["fields"]["value"] == 12.34

@pytest.mark.parametrize(
    "temperature,humidity",
    [
        (20, None),
        (None, 80),
        (None, None),
    ]
)
def test_raw(uut, sensor, data_builder, temperature, humidity):
    sensor.SGP40.return_value.raw = 5432

    uut.measure(data_builder, Measurements(temperature, humidity))

    assert len(data_builder.data) == 1
    data = data_builder.data[0]
    assert data["measurement"] == "data"
    assert "value" in data["fields"]
    assert data["fields"]["value"] == 5432.0

