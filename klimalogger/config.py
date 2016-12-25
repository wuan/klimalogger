import os
import socket

from injector import singleton, provides, Module, inject
from lazy import lazy

import configparser


@singleton
class Config(object):
    @inject(config_parser=configparser.ConfigParser)
    def __init__(self, config_parser):
        self.config_parser = config_parser

    @lazy
    def client_location_name(self) -> str:
        return self.config_parser.get('client', 'location_name')

    @lazy
    def client_host_name(self) -> str:
        return socket.gethostname()

    @lazy
    def store_username(self) -> str:
        return self.config_parser.get('store', 'username')

    @lazy
    def store_password(self) -> str:
        return self.config_parser.get('store', 'password')

    @lazy
    def store_name(self) -> str:
        return self.config_parser.get('store', 'name')

    @lazy
    def store_host(self) -> str:
        return self.config_parser.get('store', 'host')

    @lazy
    def store_port(self) -> int:
        port_string = self.config_parser.get('store', 'port')
        return int(port_string)

    @lazy
    def log_path(self) -> str:
        return self.config_parser.get('log', 'path')


class ConfigModule(Module):
    @singleton
    @provides(configparser.ConfigParser)
    def provide_config_parser(self):

        config_file_locations = ['/etc/klimalogger/klimalogger.conf', '/etc/klimalogger.conf']

        for config_file_location in config_file_locations:
            if os.path.exists(config_file_location):
                print(("reading config file location", config_file_location))
                config_parser = configparser.ConfigParser()
                config_parser.read(config_file_location)
                return config_parser

        raise IOError("config file not found")
