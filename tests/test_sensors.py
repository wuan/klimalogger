from unittest import mock

import pytest

from klimalogger.config import Config
from klimalogger.sensors import Sensors, scan


class DummySensor:
    def __init__(self, name: str, priority: int, behavior: str = "ok"):
        self.name = name
        self.priority = priority
        self._behavior = behavior

    # Sensors.measure calls this
    def measure(self, data_builder, measurements):
        if self._behavior == "raise_oserror":
            raise OSError("I2C bus error")
        # add a deterministic record so we can assert it was called
        data_builder.add(self.name, "dummy", "u", 1)


@pytest.fixture
def sensor_map(monkeypatch):
    # Build a temporary sensor_map with two dummy sensor factories
    temp_map = {
        "S1": lambda i2c_bus, address, config: DummySensor("S1", priority=2),
        "S2": lambda i2c_bus, address, config: DummySensor("S2", priority=1),
        "S_ERR": lambda i2c_bus, address, config: DummySensor(
            "S_ERR", priority=3, behavior="raise_oserror"
        ),
    }
    monkeypatch.setattr(Sensors, "sensor_map", temp_map, raising=True)
    return temp_map


def test_scan_retries_until_devices_found(monkeypatch):
    # Prepare a fake I2C bus that locks after first attempt and returns devices after a few scans
    i2c_bus = mock.MagicMock()

    # try_lock returns True immediately
    i2c_bus.try_lock.return_value = True

    scans = [[], [], [0x10, 0x11]]

    def fake_scan():
        return scans.pop(0) if scans else [0x10, 0x11]

    i2c_bus.scan.side_effect = fake_scan

    # Avoid real sleeping to keep tests fast
    monkeypatch.setattr("time.sleep", lambda _: None)

    devices = scan(i2c_bus)

    assert devices == [0x10, 0x11]
    # ensure it unlocked once done
    i2c_bus.unlock.assert_called_once()
    # ensure scan was called at least twice due to retries
    assert i2c_bus.scan.call_count >= 2


def test_sensors_init_uses_config_sensors_and_priority_sort(
    monkeypatch, sensor_map, i2c_bus, data_builder
):
    # Use config.sensors to avoid invoking scan()
    cfg = Config(
        mqtt_host="h",
        mqtt_port=1883,
        mqtt_prefix="p",
        sensors=[0x10, 0x11],
        device_map={0x10: "S1", 0x11: "S2"},
    )

    # Ensure top-level scan() is not called when config.sensors is provided
    def fail_scan(_):  # pragma: no cover - should never be called
        raise AssertionError("scan() must not be called when config.sensors is set")

    monkeypatch.setattr("klimalogger.sensors.scan", fail_scan, raising=True)

    uut = Sensors(config=cfg, i2c_bus=i2c_bus)

    # Two sensors are created and sorted by priority (S2 has priority 1, S1 has 2)
    names_in_order = [s.name for s in uut.sensors]
    assert names_in_order == ["S2", "S1"]

    # measure() runs each sensor and adds a timing entry per successful sensor
    out = uut.measure(data_builder)

    # Our DummySensor adds one deterministic record each
    types = [e["tags"]["type"] for e in out.data]
    assert types.count("dummy") == 2
    # And there should be a timing record for each sensor
    assert types.count("time") == 2
    # time entries have unit ms
    time_units = [e["tags"]["unit"] for e in out.data if e["tags"]["type"] == "time"]
    assert all(u == "ms" for u in time_units)


def test_sensors_measure_suppresses_oserror(
    monkeypatch, sensor_map, i2c_bus, data_builder
):
    # One good sensor and one that raises OSError
    cfg = Config(
        mqtt_host="h",
        mqtt_port=1883,
        mqtt_prefix="p",
        sensors=[0x20, 0x21],
        device_map={0x20: "S2", 0x21: "S_ERR"},
    )

    uut = Sensors(config=cfg, i2c_bus=i2c_bus)

    out = uut.measure(data_builder)

    # Only the good sensor contributes data and time; the failing one is skipped entirely
    types = [e["tags"]["type"] for e in out.data]
    assert types.count("dummy") == 1
    assert types.count("time") == 1
    # Ensure the successful sensor is S2
    sensors = {e["tags"]["sensor"] for e in out.data}
    assert "S2" in sensors and "S_ERR" not in sensors
