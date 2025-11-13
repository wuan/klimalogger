import busio

# Imported only for type checking to avoid circular imports at runtime
from ..data_builder import DataBuilder
from ..measurement import Measurements


class BaseSensor:
    """Common base class for all sensors.

    Provides a shared interface and common attributes that all sensors expose.
    Subclasses must implement the `measure` method and should define `name`
    and `priority` class attributes.
    """

    # Human-readable sensor name; subclasses should override
    name: str = "Sensor"
    # Lower numbers run earlier; subclasses should override
    priority: int = 100

    def measure(
        self, data_builder: "DataBuilder", measurements: "Measurements"
    ) -> None:
        """Perform a measurement and add values via the DataBuilder.

        Implementations may also read/update `measurements` to share context
        (e.g., temperature/humidity) across sensors.
        """
        raise NotImplementedError


def create_i2c_bus() -> busio.I2C:
    import board

    return busio.I2C(board.SCL, board.SDA, frequency=100000)
