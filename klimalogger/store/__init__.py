import logging

from injector import Module, provider, singleton

from .client import StoreClient
from ..config import Config

log = logging.getLogger(__name__)

def influxdb_store_factory(config: Config):
    if config.store_org is not None:
        from .influxdb2 import InfluxDb2Store
        return InfluxDb2Store(config)
    else:
        from .influxdb import InfluxDbStore
        return InfluxDbStore(config)

class StoreModule(Module):
    @provider
    @singleton
    def store_provider(self, config: Config) -> StoreClient:
        log.info("store provider type: %s", config.store_type)

        if config.store_type == "file":
            from .file import FileStore
            return FileStore()
        elif config.store_type == 'queue':
            from .queue import QueueStore
            return QueueStore(config)
        else:
            return influxdb_store_factory(config)
