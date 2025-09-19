import pytest

from klimalogger.config import Config


@pytest.fixture
def config():
    return Config(
        mqtt_host="example.local",
        mqtt_port=1883,
        mqtt_prefix="my/prefix",
        elevation=123,
    )
