from injector import singleton, inject

from influxdb import InfluxDBClient

from . import config


@singleton
class StoreClient(object):
    @inject(configuration=config.Config)
    def __init__(self, configuration, data_log):
        self.data_log = data_log
        try:
            self.client = InfluxDBClient(
                host=configuration.store_host,
                port=configuration.store_port,
                database=configuration.store_name,
                username=configuration.store_username,
                password=configuration.store_password,
                timeout=5)
        except:
            self.client = None

    def store(self, data):
        if self.client:
            self.client.write_points(data)
        else:
            raise RuntimeError("bla")



def client():
    from . import INJECTOR

    return INJECTOR.get(StoreClient)
