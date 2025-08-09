import logging

from injector import Module, provider, singleton

from typing import Protocol, List


class StoreClient(Protocol):
    def store(self, data: List[dict]):
        ...
from ..config import Config

log = logging.getLogger(__name__)

class StoreModule(Module):
    @provider
    @singleton
    def store_provider(self, config: Config) -> StoreClient:
        log.info("store provider type: %s", config.store_type)

        if config.store_type == 'queue':
            from .queue import QueueStore
            return QueueStore(config)
        elif config.store_type == 'file':
            # FileStore has been removed. Fallback to QueueStore to maintain compatibility.
            log.warning("FileStore has been removed. Falling back to QueueStore.")
            from .queue import QueueStore
            return QueueStore(config)
        else:
            raise RuntimeError(f"Unsupported store type: {config.store_type}. Supported types: 'queue'.")
