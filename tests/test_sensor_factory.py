from functools import partial
from unittest import mock

import pytest

from klimalogger import DataBuilder, MeasurementDispatcher
from klimalogger.measurement import Measurements, SensorFactory


class TestSensorFactory:

    @pytest.fixture
    def bus_i2c(self):
        with mock.patch("busio.I2C") as bus_i2c:
            yield bus_i2c()

    @pytest.fixture
    def configuration(self):
        with mock.patch("configparser.ConfigParser") as config_parser:
            yield config_parser()

    def test_sorting(self, configuration):
        calls = []

        def register_call(*args, **kwargs):
            calls.append((kwargs.pop("caller", None), mock.call(*args, **kwargs)))
            return mock.DEFAULT

        configuration.get.return_value = "foo,bar,baz"
        foo_sensor = mock.Mock()
        foo_sensor.name = "foo"
        foo_sensor.priority = 2
        foo_sensor.measure.side_effect = partial(register_call, caller="foo")
        bar_sensor = mock.Mock()
        bar_sensor.name = "bar"
        bar_sensor.priority = 3
        bar_sensor.measure.side_effect = partial(register_call, caller="bar")
        baz_sensor = mock.Mock()
        baz_sensor.name = "baz"
        baz_sensor.priority = 1
        baz_sensor.measure.side_effect = partial(register_call, caller="baz")

        sensor_factory = mock.Mock(SensorFactory)

        def load_module(sensor_name):
            return {
                "foo": foo_sensor,
                "bar": bar_sensor,
                "baz": baz_sensor,
            }[sensor_name]

        sensor_factory.create_sensor.side_effect = load_module

        uut = MeasurementDispatcher(configuration, sensor_factory)

        uut.measure()

        assert len(calls) == 3
        # Ensure order by priority: baz (1), foo (2), bar (3)
        assert calls[0][0] == "baz"
        assert calls[1][0] == "foo"
        assert calls[2][0] == "bar"

        # All sensors should receive the same DataBuilder instance
        db0 = calls[0][1].args[0]
        db1 = calls[1][1].args[0]
        db2 = calls[2][1].args[0]
        assert isinstance(db0, DataBuilder)
        assert db0 is db1 is db2

        # And a default Measurements instance
        assert calls[0][1].args[1] == Measurements()
        assert calls[1][1].args[1] == Measurements()
        assert calls[2][1].args[1] == Measurements()
