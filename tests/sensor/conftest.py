import mock
import pytest


@pytest.fixture
def i2c_bus():
    return mock.MagicMock("i2c_bus")
