import logging

from influxdb import InfluxDBClient
from injector import inject

from .client import StoreClient
from ..config import Config

log = logging.getLogger(__name__)


class InfluxDbStore(StoreClient):
    @inject
    def __init__(self, configuration: Config):
        try:
            self.client = InfluxDBClient(
                host=configuration.store_host,
                port=configuration.store_port,
                database=configuration.store_name,
                username=configuration.store_username,
                password=configuration.store_password,
                timeout=5)
        except Exception as e:
            log.error("could not create client", e)
            self.client = None

    def store(self, data: dict):
        if self.client:
            log.info("write data")
            self.client.write_points(data)
        else:
            log.error("client not available")
            raise RuntimeError("client not available")
