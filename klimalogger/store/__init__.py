from injector import Module, provider, singleton

from .client import StoreClient
from ..config import Config


class StoreModule(Module):
    @provider
    @singleton
    def store_provider(self, config: Config) -> StoreClient:
        if config.store_type == 'queue':
            from .queue import QueueStore
            return QueueStore(config)
        else:
            from .influxdb import InfluxDbStore
            return InfluxDbStore(config)
