from injector import singleton, inject, Injector

from .config import ConfigModule
from .data_builder import DataBuilder
from .data_log import DataLog
from .measurement import MeasurementDispatcher
from .store import StoreClient
from .store import StoreModule

INJECTOR = Injector(
    [StoreModule(), ConfigModule()])


@singleton
class Client:
    @inject
    def __init__(self, data_builder: DataBuilder, measurement_dispatcher: MeasurementDispatcher, store_client: StoreClient,
                 data_log: DataLog):
        self.data_builder = data_builder
        self.measurement_dispatcher = measurement_dispatcher
        self.store_client = store_client
        self.data_log = data_log

    def measure_and_store(self):
        (timestamp, data) = self.measure()

        try:
            self.store_client.store(data)
            print("stored data")
        except Exception as e:
            print("error during data transmission: create local log entry", e)
            self.data_log.store(data, timestamp)

        self.data_log.transmit_stored_data()

    def measure(self):
        self.measurement_dispatcher.measure(self.data_builder)

        return self.data_builder.timestamp, self.data_builder.data


def client():
    return INJECTOR.get(Client)
