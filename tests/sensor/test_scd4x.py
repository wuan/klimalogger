from unittest import mock

import pytest
from mock import patch

from klimalogger.sensor.scd4x import Sensor
from klimalogger.measurement import Measurements


@pytest.fixture
def sensor_module():
    # Patch the external dependency so tests don't require the hardware library
    with patch('klimalogger.sensor.scd4x.adafruit_scd4x', autospec=True) as mock_module:
        yield mock_module


@pytest.fixture
def uut(sensor_module, i2c_bus):
    return Sensor(i2c_bus=i2c_bus)


def test_init_starts_periodic_measurement(sensor_module, i2c_bus):
    # When creating the sensor
    s = Sensor(i2c_bus=i2c_bus)

    # Then driver is constructed with given bus and periodic measurement started
    sensor_module.SCD4X.assert_called_once_with(i2c_bus)
    sensor_module.SCD4X.return_value.start_periodic_measurement.assert_called_once_with()

    # Cleanup to avoid side effects (call __del__ deterministically)
    s.__del__()


def test_del_stops_periodic_measurement(uut, sensor_module):
    # Explicitly trigger destructor logic deterministically
    uut.__del__()
    sensor_module.SCD4X.return_value.stop_periodic_measurement.assert_called_once_with()


def test_measure_co2_immediate(uut, sensor_module, data_builder):
    # Given sensor returns CO2 immediately
    sensor_module.SCD4X.return_value.CO2 = 415

    meas = Measurements()
    with patch('klimalogger.sensor.scd4x.time.sleep') as sleep_mock:
        uut.measure(data_builder, meas)
        sleep_mock.assert_not_called()

    # Then one CO2 record was added with expected tags/values
    assert len(data_builder.data) == 1
    entry = data_builder.data[0]
    assert entry["measurement"] == "data"
    assert entry["tags"]["sensor"] == "SCD4x"
    assert entry["tags"]["type"] == "CO2"
    assert entry["tags"]["unit"] == "ppm"
    assert isinstance(entry["fields"]["value"], float)
    assert entry["fields"]["value"] == 415.0


def test_measure_co2_after_wait(uut, sensor_module, data_builder):
    # Given sensor returns None once, then a value
    co2_sequence = [None, 999]

    class CO2Sequence:
        def __iter__(self):
            return self
        def __next__(self):
            if not co2_sequence:
                raise StopIteration
            return co2_sequence.pop(0)

    # Simulate property access changing over time via side_effect on attribute access
    values = [None, 999]
    def co2_getter():
        return values.pop(0)
    type(sensor_module.SCD4X.return_value).CO2 = property(lambda self: co2_getter())

    meas = Measurements()
    with patch('klimalogger.sensor.scd4x.time.sleep') as sleep_mock:
        uut.measure(data_builder, meas)
        # Should sleep exactly once due to first None
        assert sleep_mock.call_count == 1

    assert len(data_builder.data) == 1
    e = data_builder.data[0]
    assert e["tags"]["type"] == "CO2"
    assert e["tags"]["unit"] == "ppm"
    assert e["tags"]["sensor"] == "SCD4x"
    assert e["fields"]["value"] == 999.0
