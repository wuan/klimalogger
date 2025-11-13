from .logger import create_logger

log = create_logger(__name__)


class Measurements:
    def __init__(
        self, temperature: float | None = None, relative_humidity: float | None = None
    ):
        self.temperature = temperature
        self.relative_humidity = relative_humidity

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
