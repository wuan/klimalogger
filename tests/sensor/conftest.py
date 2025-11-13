from unittest import mock

import pytest

from klimalogger import DataBuilder
from klimalogger.measurement import Measurements


@pytest.fixture
def i2c_bus():
    return mock.MagicMock("i2c_bus")


@pytest.fixture
def data_builder():
    return DataBuilder()


@pytest.fixture
def measurements():
    return Measurements()


@pytest.fixture
def temp_calc():
    return mock.Mock(name="TemperatureCalc")


@pytest.fixture
def pressure_calc():
    return mock.Mock(name="PressureCalc")


@pytest.fixture
def tuv():
    """Return a helper that extracts (type, unit, value) tuples from DataBuilder records."""

    def _tuv(data):
        return [
            (e["tags"]["type"], e["tags"]["unit"], e["fields"]["value"]) for e in data
        ]

    return _tuv
