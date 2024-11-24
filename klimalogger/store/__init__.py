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
