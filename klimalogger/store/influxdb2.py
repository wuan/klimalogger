import logging
import typing
from collections.abc import Iterable
from typing import Union, List

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
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
                username=configuration.service_username,
                password=configuration.service_password,
            )
        except Exception as e:
            log.error("could not create client", exc_info=e)
            self.client = None
        self.name = configuration.service_name
        self.callbacks = BatchingCallback()
        assert self.client.ping()

    def store(self, data: Union[dict, typing.Iterable[dict]]):
        if self.client:
            assert self.client.ping()

            log.info("write data")
            if isinstance(data, Iterable):
                record = [Point.from_dict(entry) for entry in data]
            else:
                record = Point.from_dict(data)
            with self.client.write_api(
                    error_callback=self.callbacks.error,
                    retry_callback=self.callbacks.retry) as write_api:
                write_api.write(self.name, record=record)
        else:
            log.error("client not available")
            raise RuntimeError("client not available")
