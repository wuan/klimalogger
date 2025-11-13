from unittest import mock
from unittest.mock import patch

import pytest

from klimalogger.config import Config
from klimalogger.sensor.dps310 import DPS310Sensor


@pytest.fixture
def sensor():
    # Patch the class alias used inside the module under test
    with patch("klimalogger.sensor.dps310.DPS310", autospec=True) as mock_cls:
        yield mock_cls


@pytest.fixture
def uut(sensor, i2c_bus, config, pressure_calc):
    return DPS310Sensor(i2c_bus=i2c_bus, config=config, pressure_calc=pressure_calc)


def test_measure_success(
    uut, sensor, data_builder, measurements, pressure_calc, config, tuv
):
    measured_temperature = 21.23456
    measured_pressure = 1001.23456
    calculated_slp = 1012.34567

    # Configure mocked driver readings
    sensor.return_value.temperature = measured_temperature
    sensor.return_value.pressure = measured_pressure
    pressure_calc.sea_level_pressure.return_value = calculated_slp

    uut.measure(data_builder, measurements)

    # Three records expected: temperature, pressure, sea level pressure
    assert len(data_builder.data) == 3
    t = tuv(data_builder.data)

    assert ("temperature", "°C", 21.235) in t
    assert ("pressure", "hPa", 1001.235) in t
    assert ("sea level pressure", "hPa", 1012.346) in t

    # sea level pressure calculation called with raw values and elevation
    assert pressure_calc.sea_level_pressure.call_args_list == [
        mock.call(measured_pressure, measured_temperature, config.elevation)
    ]


def test_measure_without_pressure(
    uut, sensor, data_builder, measurements, pressure_calc, tuv
):
    # Temperature available but pressure is None → only temperature added
    sensor.return_value.temperature = 22.5
    sensor.return_value.pressure = None

    uut.measure(data_builder, measurements)

    assert len(data_builder.data) == 1
    assert tuv(data_builder.data) == [("temperature", "°C", 22.5)]
    pressure_calc.sea_level_pressure.assert_not_called()


def test_measure_with_zero_pressure(
    uut, sensor, data_builder, measurements, pressure_calc, tuv
):
    # Zero pressure is falsy → treated as unavailable
    sensor.return_value.temperature = 19.8765
    sensor.return_value.pressure = 0.0

    uut.measure(data_builder, measurements)

    assert len(data_builder.data) == 1
    t = tuv(data_builder.data)
    assert ("temperature", "°C", 19.877) in t
    pressure_calc.sea_level_pressure.assert_not_called()


def test_measure_no_sea_level_when_no_elevation(
    sensor, i2c_bus, pressure_calc, data_builder, measurements, tuv
):
    # elevation = 0 → falsy, so no sea level pressure calculated
    cfg = Config(
        mqtt_host="example.local",
        mqtt_port=1883,
        mqtt_prefix="my/prefix",
        elevation=0,
    )

    uut = DPS310Sensor(i2c_bus=i2c_bus, config=cfg, pressure_calc=pressure_calc)

    sensor.return_value.temperature = 20.1111
    sensor.return_value.pressure = 999.9999

    uut.measure(data_builder, measurements)

    t = tuv(data_builder.data)
    assert ("temperature", "°C", 20.111) in t
    assert ("pressure", "hPa", 1000.0) in t

    # No sea level pressure without elevation
    assert all(tp != "sea level pressure" for tp, _, _ in t)
    pressure_calc.sea_level_pressure.assert_not_called()
