import busio


def create_i2c_bus() -> busio.I2C:
    """Create and return a configured I2C bus instance.

    This replaces the previous Injector-based provider with a simple factory
    function to avoid dependency injection framework usage.
    """
    import board
    return busio.I2C(board.SCL, board.SDA, frequency=100000)
