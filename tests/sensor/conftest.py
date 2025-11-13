from unittest import mock

import pytest

from klimalogger.measurement import Measurements


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
