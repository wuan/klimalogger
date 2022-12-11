import glob
import json
import logging
import os

from injector import inject, singleton

from . import config
from .store import StoreClient

log = logging.getLogger(__name__)
@singleton
class DataLog:
    @inject
    def __init__(self, configuration: config.Config, store_client: StoreClient):
        self.log_path = configuration.log_path
        self.store_client = store_client

    def store(self, data, timestamp):
        with open(os.path.join(self.log_path, timestamp + '.json'), 'w') as output_file:
            output_file.write(json.dumps(data))

    def transmit_stored_data(self):
        data_file_names = glob.glob(os.path.join(self.log_path, '*.json'))
        data_file_names.sort()

        for data_file_name in data_file_names:
            with open(data_file_name, 'r') as input_file:
                try:
                    data = json.loads(input_file.read())
                except:
                    log.warning("error loading data %s",data_file_name)
                    continue
                log.info("%s: %s", data_file_name, data)
                try:
                    log.info("client: %s", self.store_client)
                    self.store_client.store(data)
                except Exception:
                    log.exception("transmission error of archive - skipping")
                    break
            os.unlink(data_file_name)
