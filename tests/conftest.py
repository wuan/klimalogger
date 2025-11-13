from unittest import mock

import pytest

from klimalogger import DataBuilder
from klimalogger.config import Config


@pytest.fixture
def config():
    return Config(
        mqtt_host="example.local",
        mqtt_port=1883,
        mqtt_prefix="my/prefix",
        elevation=123,
    )


@pytest.fixture
def i2c_bus():
    return mock.MagicMock("i2c_bus")


@pytest.fixture
def data_builder():
    return DataBuilder()
