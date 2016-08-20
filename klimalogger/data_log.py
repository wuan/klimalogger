import glob
import json
import os

from injector import inject, singleton

from . import config

@singleton
class DataLog(object):
    @inject(configuration=config.Config)
    def __init__(self, configuration):
        self.log_path = configuration.log_path

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
                    client.write_points(data)
                except:
                    print("transmission error of archive - skipping")
                    break
            os.unlink(data_file_name)
