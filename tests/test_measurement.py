import configparser
from types import SimpleNamespace
from unittest import mock

import pytest

from klimalogger.measurement import MeasurementDispatcher, SensorFactory


class TestMeasurementDispatcher:
    def test_measure_adds_time_entries_and_handles_sensor_errors(self, mocker):
        # Configuration lists three sensors (one will fail)
        cfg = configparser.ConfigParser()
        cfg.add_section('client')
        cfg.set('client', 'sensors', 'foo, bad , bar')

        # Prepare three fake sensors with different priorities
        foo = mock.Mock()
        foo.name = 'foo'
        foo.priority = 2
        bar = mock.Mock()
        bar.name = 'bar'
        bar.priority = 1
        bad = mock.Mock()
        bad.name = 'bad'
        bad.priority = 3
        bad.measure.side_effect = RuntimeError('boom')

        # SensorFactory that returns our fakes by name
        factory = mock.Mock(spec=SensorFactory)
        factory.create_sensor.side_effect = lambda name: {'foo': foo, 'bar': bar, 'bad': bad}[name]

        # Control time: first call is for DataBuilder timestamp, then pairs for each sensor
        # Order of execution should be by priority: bar (1), foo (2), bad (3)
        time_values = [42.0,  # DataBuilder timestamp
                       100.0, 100.05,  # bar duration -> 50.0 ms
                       200.0, 200.10,  # foo duration -> 100.0 ms
                       300.0, 300.20]  # bad duration pair won't be used because it raises
        mocker.patch('time.time', side_effect=time_values)

        uut = MeasurementDispatcher(cfg, factory)

        data_builder = uut.measure()

        # bar and foo were called; bad raised and was ignored
        assert bar.measure.called
        assert foo.measure.called
        assert bad.measure.called  # it was attempted but failed

        # DataBuilder should contain two extra time entries for successful sensors
        time_entries = [e for e in data_builder.data if e['tags']['type'] == 'time' and e['tags']['unit'] == 'ms']
        # 2 entries: bar then foo (order of entries follows sensor iteration order)
        assert len(time_entries) == 2

        # Validate sensor tags and measured durations
        # Rounding is to 0.1 ms, but our differences are exact
        assert time_entries[0]['tags']['sensor'] == 'bar'
        assert time_entries[0]['fields']['value'] == 50.0
        assert time_entries[1]['tags']['sensor'] == 'foo'
        assert time_entries[1]['fields']['value'] == 100.0


class TestSensorFactory:
    def test_create_sensor_injects_supported_deps_and_reuses_i2c_bus(self, mocker):
        # Config parser passed to factory
        cfg = configparser.ConfigParser()
        # Patch i2c bus creation
        create_bus = mocker.patch('klimalogger.measurement.create_i2c_bus', autospec=True)
        create_bus.return_value = mock.sentinel.BUS

        # Fake sensor class that only accepts i2c_bus and temperature_calc
        received_kwargs = {}

        class FakeSensor:
            def __init__(self, *, i2c_bus, temperature_calc):
                received_kwargs['i2c_bus'] = i2c_bus
                received_kwargs['temperature_calc'] = temperature_calc

        fake_module = SimpleNamespace(Sensor=FakeSensor)
        mocker.patch('importlib.import_module', return_value=fake_module)

        factory = SensorFactory(cfg)

        # First creation should create the bus and pass only supported kwargs
        sensor1 = factory.create_sensor('whatever')
        assert sensor1 is not None
        assert received_kwargs['i2c_bus'] is mock.sentinel.BUS
        assert received_kwargs['temperature_calc'] is not None  # instance provided
        create_bus.assert_called_once()

        # Second creation should reuse the same bus (no new calls)
        sensor2 = factory.create_sensor('whatever')
        assert sensor2 is not None
        create_bus.assert_called_once()

    def test_i2c_bus_failure_is_handled_and_None_is_injected(self, mocker):
        cfg = configparser.ConfigParser()
        mocker.patch('klimalogger.measurement.create_i2c_bus', side_effect=RuntimeError('no i2c'))

        # Fake sensor that tolerates i2c_bus=None
        captured = {}

        class FakeSensor:
            def __init__(self, *, i2c_bus=None, **_):
                captured['i2c_bus'] = i2c_bus

        fake_module = SimpleNamespace(Sensor=FakeSensor)
        mocker.patch('importlib.import_module', return_value=fake_module)

        factory = SensorFactory(cfg)
        sensor = factory.create_sensor('foo')
        assert sensor is not None
        assert captured['i2c_bus'] is None
