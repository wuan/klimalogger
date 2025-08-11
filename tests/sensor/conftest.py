import mock
import pytest

from klimalogger import DataBuilder
from klimalogger.measurement import Measurements


@pytest.fixture
def i2c_bus():
    return mock.MagicMock("i2c_bus")

@pytest.fixture
def data_builder():
    return DataBuilder()

@pytest.fixture
def measurements():
    return Measurements()
