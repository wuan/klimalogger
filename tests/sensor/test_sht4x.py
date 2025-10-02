from unittest import mock
from unittest.mock import patch

import pytest

from klimalogger.measurement import Measurements
from klimalogger.sensor.sht4x import SHT4xSensor


@pytest.fixture
def sensor():
    with patch("klimalogger.sensor.sht4x.adafruit_sht4x", autospec=True) as mock_module:
        yield mock_module


@pytest.fixture
def uut(sensor, i2c_bus, temp_calc):
    return SHT4xSensor(i2c_bus=i2c_bus, address=14, temperature_calc=temp_calc)


def test_measure_success(uut, sensor, data_builder, temp_calc, measurements):
    measured_temperature = 21.234
    measured_relative_humidity = 45.678
    calculated_dew_point = 12.3456
    sensor.SHT4x.return_value.measurements = (
        measured_temperature,
        measured_relative_humidity,
    )
    temp_calc.dew_point.return_value = calculated_dew_point

    uut.measure(data_builder, measurements)

    # Measurements stored and rounded
    assert measurements.temperature == 21.23
    assert measurements.relative_humidity == 45.68

    # Three records: temperature, dew point (calculated), relative humidity
    assert len(data_builder.data) == 3
    types_units_values = [
        (e["tags"]["type"], e["tags"]["unit"], e["fields"]["value"])
        for e in data_builder.data
    ]

    assert ("temperature", "°C", 21.23) in types_units_values
    assert ("dew point", "°C", 12.35) in types_units_values
    assert ("relative humidity", "%", 45.68) in types_units_values

    # Check sensor tag and calculated flag for dew point
    dew_entries = [e for e in data_builder.data if e["tags"]["type"] == "dew point"]
    assert dew_entries and dew_entries[0]["tags"]["sensor"] == "SHT4x"
    assert dew_entries[0]["tags"]["calculated"] is True

    assert temp_calc.dew_point.call_args_list == [
        mock.call(measured_temperature, measured_relative_humidity)
    ]


def test_measure_success_failed_dew_point(
    uut, sensor, data_builder, temp_calc, measurements
):
    measured_temperature = 21.234
    measured_relative_humidity = 45.678
    sensor.SHT4x.return_value.measurements = (
        measured_temperature,
        measured_relative_humidity,
    )
    temp_calc.dew_point.side_effect = [ValueError("failed")]

    uut.measure(data_builder, measurements)

    # Measurements stored and rounded
    assert measurements.temperature == 21.23
    assert measurements.relative_humidity == 45.68

    # Three records: temperature, dew point (calculated), relative humidity
    assert len(data_builder.data) == 2
    types_units_values = [
        (e["tags"]["type"], e["tags"]["unit"], e["fields"]["value"])
        for e in data_builder.data
    ]

    assert ("temperature", "°C", 21.23) in types_units_values
    assert ("relative humidity", "%", 45.68) in types_units_values

    assert temp_calc.dew_point.call_args_list == [
        mock.call(measured_temperature, measured_relative_humidity)
    ]


def test_ignores_invalid_temperature(uut, sensor, data_builder):
    # Temperature below -40 should be treated as invalid leading to no data
    sensor.SHT4x.return_value.measurements = (-45.0, 50.0)

    meas = Measurements()
    uut.measure(data_builder, meas)

    # No data added and measurements remain default
    assert data_builder.data == []
    assert meas == Measurements()
