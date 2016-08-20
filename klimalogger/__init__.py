from injector import singleton, inject, Injector

from .data_log import DataLog
from .sensor_factory import SensorFactory
from .store_client import StoreClient
from .data_builder import DataBuilder
from .config import ConfigModule

INJECTOR = Injector(
    [config.ConfigModule()])


@singleton
class Client(object):
    @inject(data_builder=DataBuilder, sensor_factory=SensorFactory, store_client=StoreClient, data_log=DataLog)
    def __init__(self, data_builder, sensor_factory, store_client, data_log):
        self.data_builder = data_builder
        self.sensor_factory = sensor_factory
        self.store_client = store_client
        self.data_log = data_log

    def measure_and_store(self):
        self.sensor_factory.measure(self.data_builder)

        data = self.data_builder.data
        timestamp = self.data_builder.timestamp
        try:
            self.store_client.store(data)
            print("stored data")
        except Exception as e:
            print("error during data transmission: create local log entry", e)
            self.data_log.store(data, timestamp)

        self.data_log.transmit_stored_data()


def client():
    return INJECTOR.get(Client)
