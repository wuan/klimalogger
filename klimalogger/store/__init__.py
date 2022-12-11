import logging

from injector import Module, provider, singleton

from .client import StoreClient
from ..config import Config

log = logging.getLogger(__name__)

class StoreModule(Module):
    @provider
    @singleton
    def store_provider(self, config: Config) -> StoreClient:
        log.info("store provider type: %s", config.store_type)

        if config.store_type == 'queue':
            from .queue import CombinedStore
            return CombinedStore(config)
        else:
            from .influxdb import InfluxDbStore
            return InfluxDbStore(config)
