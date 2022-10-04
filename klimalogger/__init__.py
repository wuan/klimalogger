import logging
import time

from injector import singleton, inject, Injector

from .config import ConfigModule, Config
from .data_builder import DataBuilder
from .data_log import DataLog
from .measurement import MeasurementDispatcher
from .sensor import SensorModule
from .store import StoreClient
from .store import StoreModule
from . import logger

INJECTOR = Injector(
    [StoreModule(), ConfigModule(), SensorModule()])

root_logger = logging.getLogger(__name__)
root_logger.setLevel(logging.WARN)

log = root_logger


def set_log_level(log_level):
    root_logger.setLevel(log_level)


def add_log_handler(log_handler):
    root_logger.addHandler(log_handler)


def set_parent_logger(logger):
    logger.parent = root_logger


@singleton
class Client:
    @inject
    def __init__(self, measurement_dispatcher: MeasurementDispatcher,
                 store_client: StoreClient,
                 data_log: DataLog,
                 config: Config):
        self.measurement_dispatcher = measurement_dispatcher
        self.store_client = store_client
        self.data_log = data_log
        self.config = config

    def measure_and_store_periodically(self, period=30):
        log.info("measure_and_store_periodically(%d)", period)
        last_measurement = time.time() - period
        while True:
            timestamp = time.time()
            if last_measurement < timestamp - period:
                self.measure_and_store()
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
        result = self.measurement_dispatcher.measure()

        return result.timestamp, result.data

    def store_data(self, data, timestamp):
        try:
            self.store_client.store(data)
            log.info("stored data")
        except Exception as e:
            log.error("error during data transmission: create local log entry", e)
            self.data_log.store(data, timestamp)
        self.data_log.transmit_stored_data()


def client():
    return INJECTOR.get(Client)
