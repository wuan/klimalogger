import os


class Config:

    @property
    def mqtt_host(self):
        return os.getenv("MQTT_HOST")

    @property
    def mqtt_port(self):
        return int(os.getenv("MQTT_PORT", "1883"))

    @property
    def mqtt_prefix(self):
        return os.getenv("MQTT_PREFIX", "sensors")

    @property
    def location_name(self):
        return os.getenv("LOCATION_NAME")

    @property
    def elevation(self):
        return int(os.getenv("ELEVATION", "0"))

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
