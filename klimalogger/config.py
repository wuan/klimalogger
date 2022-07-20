import configparser
import socket
from pathlib import Path

from injector import singleton, provider, Module, inject
from lazy import lazy


@singleton
class Config(object):
    @inject
    def __init__(self, config_parser: configparser.ConfigParser):
        self.config_parser = config_parser

    @lazy
    def client_location_name(self) -> str:
        return self.config_parser.get('client', 'location_name')

    @lazy
    def client_host_name(self) -> str:
        return socket.gethostname()

    @lazy
    def store_type(self) -> str:
        return self.config_parser.get('store', 'type', fallback='direct')

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
    def queue_username(self) -> str:
        return self.config_parser.get('queue', 'username')

    @lazy
    def queue_password(self) -> str:
        return self.config_parser.get('queue', 'password')

    @lazy
    def queue_host(self) -> str:
        return self.config_parser.get('queue', 'host')

    @lazy
    def queue_port(self) -> int:
        port_string = self.config_parser.get('queue', 'port')
        return int(port_string)

    @lazy
    def queue_virtual_host(self) -> str:
        return self.config_parser.get('queue', 'virtual_host')

    @lazy
    def log_path(self) -> str:
        return self.config_parser.get('log', 'path')


class ConfigModule(Module):
    @singleton
    @provider
    def provide_config_parser(self) -> configparser.ConfigParser:
        etc = Path("/etc")
        config_filename = "klimalogger.conf"

        config_file_locations = [Path(config_filename), etc / "klimalogger" / config_filename, etc / config_filename]

        for config_file_location in config_file_locations:
            if config_file_location.exists():
                print("reading config file location", config_file_location)
                config_parser = configparser.ConfigParser()
                config_parser.read(config_file_location)
                return config_parser

        raise IOError("config file not found")
