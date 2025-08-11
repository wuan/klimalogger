import sys
import types
from unittest import mock

import pytest

from klimalogger.data_builder import DataBuilder
from klimalogger.measurement import Measurements


@pytest.fixture
def fake_hw_modules(monkeypatch):
    # Provide minimal dummy modules so import of sht4x_sensor succeeds without real hardware libs
    adafruit = types.ModuleType("adafruit_sht4x")
    # Placeholder; will be monkeypatched per test
    class _Dummy:
        pass
    adafruit.SHT4x = _Dummy

    busio = types.ModuleType("busio")
    class I2C:
        pass
    busio.I2C = I2C

    monkeypatch.setitem(sys.modules, "adafruit_sht4x", adafruit)
    monkeypatch.setitem(sys.modules, "busio", busio)

    return adafruit, busio


def import_sht4x_sensor():
    import importlib
    return importlib.import_module("klimalogger.sensor.sht4x_sensor")


def test_sht4x_measure_success(fake_hw_modules, monkeypatch):
    s = import_sht4x_sensor()

    # Prepare driver mock to return measurements
    driver = mock.Mock()
    driver.measurements = (21.234, 45.678)

    # Patch constructor to return our driver
    monkeypatch.setattr(s.adafruit_sht4x, "SHT4x", lambda i2c: driver)

    # Fake temperature calculator with predictable rounding
    class FakeTempCalc:
        def dew_point(self, temperature, rh):
            # Return a value that will be rounded to 12.35
            return 12.3456

    sensor = s.Sensor(i2c_bus=mock.Mock(), temperature_calc=FakeTempCalc())

    db = DataBuilder()
    meas = Measurements()

    sensor.measure(db, meas)

    # Measurements stored and rounded
    assert meas.temperature == 21.23
    assert meas.relative_humidity == 45.68

    # Three records: temperature, dew point (calculated), relative humidity
    types_units_values = [(e["tags"]["type"], e["tags"]["unit"], e["fields"]["value"]) for e in db.data]

    assert ("temperature", "°C", 21.23) in types_units_values
    assert ("dew point", "°C", 12.35) in types_units_values
    assert ("relative humidity", "%", 45.68) in types_units_values

    # Check sensor tag and calculated flag for dew point
    dew_entries = [e for e in db.data if e["tags"]["type"] == "dew point"]
    assert dew_entries and dew_entries[0]["tags"]["sensor"] == "SHT4x"
    assert dew_entries[0]["tags"]["calculated"] is True


def test_sht4x_measure_ignores_invalid_temperature(fake_hw_modules, monkeypatch):
    s = import_sht4x_sensor()

    driver = mock.Mock()
    driver.measurements = (-45.0, 50.0)  # Below threshold -> treated as invalid
    monkeypatch.setattr(s.adafruit_sht4x, "SHT4x", lambda i2c: driver)

    class FakeTempCalc:
        def dew_point(self, temperature, rh):
            return 10.0

    sensor = s.Sensor(i2c_bus=mock.Mock(), temperature_calc=FakeTempCalc())

    db = DataBuilder()
    meas = Measurements()

    sensor.measure(db, meas)

    # No data added and measurements remain default
    assert db.data == []
    assert meas == Measurements()
