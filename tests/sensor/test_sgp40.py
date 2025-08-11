import sys
import types
from unittest import mock

import pytest

from klimalogger.data_builder import DataBuilder
from klimalogger.measurement import Measurements


@pytest.fixture
def fake_hw_modules(monkeypatch):
    # Provide minimal dummy modules so import of sgp40_sensor succeeds without real hardware libs
    adafruit = types.ModuleType("adafruit_sgp40")
    # Placeholder; will be monkeypatched per test
    class _Dummy:
        pass
    adafruit.SGP40 = _Dummy

    busio = types.ModuleType("busio")
    class I2C:
        pass
    busio.I2C = I2C

    monkeypatch.setitem(sys.modules, "adafruit_sgp40", adafruit)
    monkeypatch.setitem(sys.modules, "busio", busio)

    return adafruit, busio


def import_sgp40_sensor():
    import importlib
    return importlib.import_module("klimalogger.sensor.sgp40_sensor")


def test_sgp40_measure_with_temp_and_humidity(fake_hw_modules, monkeypatch):
    s = import_sgp40_sensor()

    # Prepare driver mock to return a VOC index when called with T and RH
    driver = mock.Mock()
    driver.measure_index.return_value = 123.456

    # Patch constructor to return our driver
    monkeypatch.setattr(s.adafruit_sgp40, "SGP40", lambda i2c: driver)

    sensor = s.Sensor(i2c_bus=mock.Mock())

    db = DataBuilder()
    meas = Measurements(temperature=22.5, relative_humidity=55.0)

    sensor.measure(db, meas)

    # Ensure driver was called with the right compensation values
    driver.measure_index.assert_called_once_with(temperature=22.5, relative_humidity=55.0)

    # One record added for VOC index
    assert len(db.data) == 1
    entry = db.data[0]
    assert entry["tags"]["sensor"] == "SGP40"
    assert entry["tags"]["type"] == "VOC index"
    assert entry["tags"]["unit"] == ""
    assert entry["fields"]["value"] == pytest.approx(123.456)


def test_sgp40_measure_without_temp_or_humidity_uses_raw(fake_hw_modules, monkeypatch):
    s = import_sgp40_sensor()

    driver = mock.Mock()
    # raw is read directly as a value
    driver.raw = 789.123

    monkeypatch.setattr(s.adafruit_sgp40, "SGP40", lambda i2c: driver)

    sensor = s.Sensor(i2c_bus=mock.Mock())

    db = DataBuilder()
    meas = Measurements()  # temperature and RH are None

    sensor.measure(db, meas)

    # measure_index should not be called when no compensation values present
    assert not driver.measure_index.called

    assert len(db.data) == 1
    entry = db.data[0]
    assert entry["tags"]["sensor"] == "SGP40"
    assert entry["tags"]["type"] == "raw gas"
    assert entry["tags"]["unit"] == ""
    assert entry["fields"]["value"] == pytest.approx(789.123)
