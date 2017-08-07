import glob
import json
import os

from injector import inject, singleton

from .store import StoreClient
from . import config


@singleton
class DataLog(object):
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
                    print("error loading data {}".format(data_file_name))
                    continue
                print("{}: {}".format(data_file_name, data))
                try:
                    print("client:", self.store_client)
                    self.store_client.store(data)
                except Exception as e:
                    print("transmission error of archive - skipping", e)
                    break
            os.unlink(data_file_name)
