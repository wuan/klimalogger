from abc import ABCMeta, abstractmethod

from injector import Module, provider, singleton

from ..config import Config
from .client import StoreClient


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
