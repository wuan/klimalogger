import logging

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS
from injector import inject

from .client import StoreClient
from ..config import Config

log = logging.getLogger(__name__)


class BatchingCallback:
    def error(self, conf: (str, str, str), data: str, exception: InfluxDBError):
        print(f"Cannot write batch: {conf}, data: {data} due: {exception}")

    def retry(self, conf: (str, str, str), data: str, exception: InfluxDBError):
        print(f"Retryable error occurs for batch: {conf}, data: {data} retry: {exception}")


class InfluxDb2Store(StoreClient):
    @inject
    def __init__(self, configuration: Config):
        try:
            self.client = InfluxDBClient(
                url=configuration.store_url,
                org=configuration.store_org,
                username=configuration.store_username,
                password=configuration.store_password,
            )
        except Exception as e:
            log.error("could not create client", exc_info=e)
            self.client = None
        self.name = configuration.store_name
        self.callbacks = BatchingCallback()
        assert self.client.ping()


    def store(self, data: dict):
        if self.client:
            assert self.client.ping()

            log.info("write data")
            point = Point.from_dict(data)
            with self.client.write_api(
                                  error_callback=self.callbacks.error,
                                  retry_callback=self.callbacks.retry) as write_api:
                write_api.write(self.name, record=point)
        else:
            log.error("client not available")
            raise RuntimeError("client not available")




