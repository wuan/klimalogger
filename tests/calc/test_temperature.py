import pytest
from assertpy import assert_that

from klimalogger.calc import TemperatureCalc


class TestCalcTemperature:

    @pytest.fixture
    def uut(self):
        return TemperatureCalc()

    @pytest.mark.parametrize("temperature,relative_humidity,expected", [
        (20, 80, 16.444),
        (25, 10, -8.75),
        (50, 90, 47.9)
    ])
    def test_dew_point(self, uut, temperature, relative_humidity, expected):
        result = uut.dew_point(temperature, relative_humidity)

        assert_that(result).is_close_to(expected, 0.01)
