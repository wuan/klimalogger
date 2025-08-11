import pytest
from assertpy import assert_that

from klimalogger.calc import PressureCalc


class TestCalcTemperature:

    @pytest.fixture
    def uut(self):
        return PressureCalc()

    def test_sea_level_value(self, uut):
        result = uut.sea_level_pressure(1000, 20, 0)

        assert_that(result).is_close_to(1000, 0.01)

    def test_elevation_value(self, uut):
        result = uut.sea_level_pressure(943.71, 20, 500)

        assert_that(result).is_close_to(1000, 0.01)
