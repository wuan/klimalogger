try:
    import logging

    root_logger = logging.getLogger(__name__)
    root_logger.setLevel(logging.WARN)

    log = root_logger
except ImportError:
    import adafruit_logging

    log = adafruit_logging.Logger(__name__)

import time

from .config import Config, build_config
from .data_builder import DataBuilder
from .sensors import Sensors
from .transport import QueueTransport


def set_log_level(log_level):
    root_logger.setLevel(log_level)


def add_log_handler(log_handler):
    root_logger.addHandler(log_handler)


def set_parent_logger(logger):
    logger.parent = root_logger


class Client:
    def __init__(self, sensors: Sensors, transport: QueueTransport):
        self.sensors = sensors
        self.transport = transport

    def measure_and_store_periodically(self, period=15):
        log.info("measure_and_store_periodically(%d)", period)
        last_measurement = time.time() - period
        skip_initial = 2
        while True:
            timestamp = time.time()
            if last_measurement < timestamp - period:
                if skip_initial == 0:
                    self.measure_and_store()
                else:
                    log.info("skipping initial measurement(%d)", skip_initial)
                    self.measure()
                    skip_initial -= 1
                last_measurement += period
            else:
                self.measure()
            log.debug("time taken: %d", time.time() - last_measurement)
            time.sleep(1)

    def measure_and_store(self):
        log.info(
            "measure_and_store()",
        )
        data_builder = self.measure()

        self.store_data(data_builder.data)

    def measure(self):
        return self.sensors.measure()

    def store_data(self, data):
        try:
            self.transport.store(data)
            log.info("stored data")
        except Exception as e:
            log.error(
                "error during data transmission: create local log entry", exc_info=e
            )


def client():
    import board

    # Manual wiring instead of Injector
    config = build_config()
    sensors = Sensors(config, board.I2C())
    store = QueueTransport(config)
    return Client(sensors, store)


__all__ = ["client", "Config", "DataBuilder"]
