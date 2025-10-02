import configparser
import sys
import types
from unittest.mock import patch

import pytest

from klimalogger.data_builder import DataBuilder
from klimalogger.measurement import Measurements
from klimalogger.sensor.sgp30 import SGP30Sensor

# Provide a dummy 'board' module to satisfy import in sensor implementation on non-supported platforms
sys.modules.setdefault("board", types.ModuleType("board"))


@pytest.fixture
def sensor_module():
    # Patch the external dependency so tests don't require the hardware library
    with patch("klimalogger.sensor.sgp30.adafruit_sgp30", autospec=True) as mock_module:
        yield mock_module


@pytest.fixture
def config_parser():
    cp = configparser.ConfigParser()
    cp.add_section("sgp30_sensor")
    cp.set("sgp30_sensor", "baseline_eCO2", "12345")
    cp.set("sgp30_sensor", "baseline_TVOC", "678")
    return cp


@pytest.fixture
def uut(sensor_module, i2c_bus, config):
    return SGP30Sensor(i2c_bus=i2c_bus, config=config)


@pytest.fixture
def data_builder():
    return DataBuilder()


@pytest.fixture
def config(config):
    config.baselines["eCO2"] = 12.34
    config.baselines["TVOC"] = 56.78
    return config


def test_init_constructs_driver_and_parses_baselines(
    uut, sensor_module, i2c_bus, config_parser
):

    # Driver constructed with given bus
    sensor_module.Adafruit_SGP30.assert_called_once_with(i2c_bus)

    # Baselines parsed as ints from configuration
    assert uut.baseline_eCO2 == 12.34
    assert uut.baseline_TVOC == 56.78


def test_measure_adds_eCO2_and_TVOC(uut, sensor_module, data_builder):
    # Given hardware returns values
    sensor_module.Adafruit_SGP30.return_value.iaq_measure.return_value = (401, 7)

    # When
    uut.measure(data_builder, Measurements())

    # Then: two records added
    assert len(data_builder.data) == 2

    # Collect types/units/values for assertions
    types_units_values = [
        (e["tags"]["type"], e["tags"]["unit"], e["fields"]["value"])
        for e in data_builder.data
    ]

    assert ("eCO2", "ppm", 401.0) in types_units_values
    assert ("TVOC", "ppb", 7.0) in types_units_values

    # Check sensor tag
    for e in data_builder.data:
        assert e["measurement"] == "data"
        assert e["tags"]["sensor"] == "SGP30"
