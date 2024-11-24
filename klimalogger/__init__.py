import logging
import time


from .i2c import i2c_bus, Sensors
from .config import Config
from .data_builder import DataBuilder
from .measurements import MeasurementDispatcher
from .sensor import SensorModule
from .store import StoreClient
from . import logger


root_logger = logging.getLogger(__name__)
root_logger.setLevel(logging.WARN)

log = root_logger


def set_log_level(log_level):
    root_logger.setLevel(log_level)


def add_log_handler(log_handler):
    root_logger.addHandler(log_handler)


def set_parent_logger(logger):
    logger.parent = root_logger


class Client:
    def __init__(self, sensors: Sensors,
                 store_client: StoreClient,
                 config: Config):
        self.sensors = sensors
        self.store_client = store_client
        self.config = config

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
            log.info("time taken: %d", time.time() - last_measurement)
            time.sleep(1)

    def measure_and_store(self):
        log.info("measure_and_store()", )
        (timestamp, data) = self.measure()

        self.store_data(data, timestamp)

    def measure(self):
        return self.sensors.measure()

    def store_data(self, data, timestamp):
        try:
            self.store_client.store(data)
            log.info("stored data")
        except Exception as e:
            log.error("error during data transmission: create local log entry", e)


def client():
    config = Config()
    i2c_bus = i2c.i2c_bus()
    sensors = i2c.Sensors(config, i2c_bus)
    MeasurementDispatcher(sensors)

    return Client(config, sensors, store_client)

