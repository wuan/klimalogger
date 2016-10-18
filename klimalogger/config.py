import os

from injector import singleton, provides, Module, inject
from lazy import lazy

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


@singleton
class Config(object):
    @inject(config_parser=configparser.ConfigParser)
    def __init__(self, config_parser):
        self.config_parser = config_parser

    @lazy
    def client_location_name(self):
        return self.config_parser.get('client', 'location_name')

    @lazy
    def store_username(self):
        return self.config_parser.get('store', 'username')

    @lazy
    def store_password(self):
        return self.config_parser.get('store', 'password')

    @lazy
    def store_name(self):
        return self.config_parser.get('store', 'name')

    @lazy
    def store_host(self):
        return self.config_parser.get('store', 'host')

    @lazy
    def store_port(self):
        return int(self.config_parser.get('store', 'port'))

    @lazy
    def log_path(self):
        return self.config_parser.get('log', 'path')


class ConfigModule(Module):
    @singleton
    @provides(configparser.ConfigParser)
    def provide_config_parser(self):

        config_file_locations = ['/etc/klimalogger/klimalogger.conf', '/etc/klimalogger.conf']

        for config_file_location in config_file_locations:
            if os.path.exists(config_file_location):
                config_parser = configparser.ConfigParser()
                config_parser.read(config_file_location)
                return config_parser

        raise IOError("config file not found")
