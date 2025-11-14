import board
import busio


def i2c_bus_factory() -> busio.I2C | None:
    try:
        return board.STEMMA_I2C()
    except Exception as e:
        print("i2c setup failed:", e)
        return None
