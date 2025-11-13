import os
import sys

from .logger import create_logger

log = create_logger(__name__)


class Config:

    def __init__(self, **kwargs):
        self.mqtt_prefix: str = kwargs["mqtt_host"]
        self.mqtt_host: str = kwargs["mqtt_host"]
        self.mqtt_port: int = int(kwargs["mqtt_port"])
        self.mqtt_prefix: str = kwargs["mqtt_prefix"]
        self.mqtt_qos: int = kwargs.get("mqtt_qos", 1)
        self.mqtt_username: str | None = kwargs.get("mqtt_username")
        self.mqtt_password: str | None = kwargs.get("mqtt_password")
        self.host_name: str | None = kwargs.get("host_name")
        self.sensors: list[int] | None = kwargs.get("sensors")
        self.elevation: int | None = kwargs.get("elevation")
        self.baselines: dict[str, float] = kwargs.get("baselines", {})
        self.device_map: dict[int, str] = kwargs.get("device_map", {})


def is_circuitpython():
    return sys.implementation.name == "circuitpython"


def ensure_not_none(value, name: str = ""):
    if value is None:
        raise ValueError(f"{name} is required")
    return value


def build_config() -> Config:
    if is_circuitpython():
        return build_env_based_config()
    else:
        cfg = build_file_based_config()
        # Ensure we always return a valid Config instance
        if not isinstance(cfg, Config):
            raise RuntimeError("Invalid configuration")
        return cfg


def device_map(value: str) -> dict[int, str]:
    return {
        int(elements[0]): elements[1]
        for entry in value.split(",")
        if len(elements := entry.split("=")) > 1
    }


def sensors(value: str | None) -> list[int] | None:
    return (
        [int(address, 16) for address in value.split(",")]
        if value is not None
        else None
    )


def build_env_based_config():
    return Config(
        mqtt_host=ensure_not_none(os.getenv("MQTT_HOST")),
        mqtt_port=int(os.getenv("MQTT_PORT", 1883)),
        mqtt_prefix=os.getenv("MQTT_PREFIX"),
        mqtt_username=os.getenv("MQTT_USERNAME", None),
        mqtt_password=os.getenv("MQTT_PASSWORD", None),
        elevation=int(os.getenv("ELEVATION", "0")),
        device_map=device_map(os.getenv("DEVICE_MAP", "")),
    )


def build_file_based_config():
    import socket

    config_parser = load_config_parser()

    return Config(
        host_name=socket.gethostname(),
        mqtt_host=ensure_not_none(config_parser.get("queue", "host"), "queue host"),
        mqtt_port=int(config_parser.get("queue", "port")),
        mqtt_prefix=config_parser.get("queue", "queue_prefix", fallback="sensors"),
        mqtt_qos=int(config_parser.get("queue", "queue_qos", fallback="1")),
        mqtt_username=config_parser.get("queue", "username", fallback=None),
        mqtt_password=config_parser.get("queue", "password", fallback=None),
        elevation=int(config_parser.get("client", "elevation", fallback="0")),
        sensors=sensors(config_parser.get("client", "sensors", fallback=None)),
        device_map=device_map(config_parser.get("client", "device_map", fallback="")),
    )


def load_config_parser():
    import configparser
    from pathlib import Path

    """Load the configuration from standard locations, replacing the Injector-based provider."""
    etc = Path("/etc")
    config_filename = "klimalogger.conf"

    config_file_locations = [
        Path(config_filename),
        etc / "klimalogger" / config_filename,
        etc / config_filename,
    ]

    for config_file_location in config_file_locations:
        if config_file_location.exists():
            log.info("reading config file location %s", config_file_location)
            config_parser = configparser.ConfigParser()
            config_parser.read(config_file_location)
            return config_parser

    raise OSError("config file not found")
