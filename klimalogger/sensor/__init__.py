import busio
from injector import Module, singleton, provider


class SensorModule(Module):
    @singleton
    @provider
    def provide_i2c_bus(self) -> busio.I2C:
        import board
        return busio.I2C(board.SCL, board.SDA, frequency=100000)
