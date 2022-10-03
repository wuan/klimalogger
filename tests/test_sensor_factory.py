from functools import partial

import mock
import pytest

from klimalogger import MeasurementDispatcher, DataBuilder
from klimalogger.data_builder import DataBuilderFactory
from klimalogger.measurement import SensorFactory, Measurements


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
            calls.append((kwargs.pop('caller', None), mock.call(*args, **kwargs)))
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



        data_builder_factory = mock.Mock(spec=DataBuilderFactory)
        uut = MeasurementDispatcher(configuration, sensor_factory, data_builder_factory)

        uut.measure()

        assert len(calls) == 3
        assert calls[0] == ("baz", mock.call(data_builder_factory.get(), Measurements()))
        assert calls[1] == ("foo", mock.call(data_builder_factory.get(), Measurements()))
        assert calls[2] == ("bar", mock.call(data_builder_factory.get(), Measurements()))
