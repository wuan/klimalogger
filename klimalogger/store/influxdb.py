from injector import singleton, inject

from influxdb import InfluxDBClient

from klimalogger import config
from .client import StoreClient


class InfluxDbStore(StoreClient):
    @inject(configuration=config.Config)
    def __init__(self, configuration):
        try:
            self.client = InfluxDBClient(
                host=configuration.store_host,
                port=configuration.store_port,
                database=configuration.store_name,
                username=configuration.store_username,
                password=configuration.store_password,
                timeout=5)
        except Exception as e:
            print("could not create client", e)
            self.client = None

    def store(self, data: dict):
        if self.client:
            print("write data")
            self.client.write_points(data)
        else:
            print("client not available")
            raise RuntimeError("bla")
