import configparser
import logging
import os
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


class Config:

    def __init__(self):
        etc = Path("/etc")
        config_filename = "klimalogger.conf"

        config_file_locations = [Path(config_filename), etc / "klimalogger" / config_filename, etc / config_filename]

        for config_file_location in config_file_locations:
            if config_file_location.exists():
                log.info("reading config file location %s", config_file_location)
                self.config_parser = configparser.ConfigParser()
                self.config_parser.read(config_file_location)

    @property
    def service_host(self) -> str:
        return self.config_parser.get('store', 'host') if self.config_parser else os.getenv("MQTT_HOST")

    @property
    def service_port(self):
        return int(self.config_parser.get('store', 'port') if self.config_parser else os.getenv("MQTT_PORT", "1883"))

    @property
    def queue_prefix(self):
        return self.config_parser.get('store', 'queue_prefix', fallback='sensors') if self.config_parser else os.getenv("MQTT_PREFIX", "sensors")

    @property
    def location_name(self):
        return os.getenv("LOCATION_NAME")

    @property
    def elevation(self):
        return int(os.getenv("ELEVATION", "0"))

    @property
    def store_org(self) -> Optional[str]:
        return self.config_parser.get('store', 'org', fallback=None) if self.config_parser else None

    @property
    def device_map(self):
        device_map = os.getenv("DEVICE_MAP", None)
        if device_map is not None:
            entries = device_map.split(",")
            device_map = {}
            for entry in entries:
                address, name = entry.split("=")
                device_map[int(address)] = name
        return device_map

    @property
    def store_type(self):
        return self.config_parser.get('store', 'type', fallback='direct') if self.config_parser else "queue"
