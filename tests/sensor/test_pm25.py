from unittest.mock import patch

import pytest

from klimalogger.sensor.pm25 import PM25Sensor


@pytest.fixture
def sensor():
    with patch("klimalogger.sensor.pm25.PM25_I2C", autospec=True) as mock_cls:
        yield mock_cls


@pytest.fixture
def uut(sensor, i2c_bus):
    return PM25Sensor(i2c_bus=i2c_bus)


def test_measure_success(uut, sensor, data_builder, measurements, tuv):
    # Prepare a full set of keys, with some intentionally missing to test optionality
    aqdata = {
        "particles 03um": 123,
        "particles 05um": 45,
        # "particles 10um" missing on purpose
        "particles 25um": 6,
        "particles 50um": 0,
        # "particles 100um" missing
        "pm03 standard": 3.14,
        "pm05 standard": 2.72,
        "pm10 standard": 1.0,
        # "pm25 standard" missing
        "pm50 standard": 0.0,
        # "pm100 standard" missing
    }
    sensor.return_value.read.return_value = aqdata

    uut.measure(data_builder, measurements)

    t = tuv(data_builder.data)

    # Particles counts ("#") where present
    assert ("particles_03", "#", 123) in t
    assert ("particles_05", "#", 45) in t
    assert all(tp != "particles_10" for tp, _, _ in t)
    assert ("particles_25", "#", 6) in t
    assert ("particles_50", "#", 0) in t
    assert all(tp != "particles_100" for tp, _, _ in t)

    # Standard PM concentrations ("ug/m^3") where present
    assert ("part_con_03", "ug/m^3", 3.14) in t
    assert ("part_con_05", "ug/m^3", 2.72) in t
    assert ("part_con_10", "ug/m^3", 1.0) in t
    assert all(tp != "part_con_25" for tp, _, _ in t)
    assert ("part_con_50", "ug/m^3", 0.0) in t
    assert all(tp != "part_con_100" for tp, _, _ in t)


def test_measure_runtime_error_returns_without_data(
    uut, sensor, data_builder, measurements
):
    sensor.return_value.read.side_effect = RuntimeError("I2C error")

    uut.measure(data_builder, measurements)

    assert data_builder.data == []
