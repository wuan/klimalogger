import datetime

from injector import singleton, inject

from .config import Config


@singleton
class DataBuilder(object):
    @inject
    def __init__(self, configuration: Config):
        self.location = configuration.client_location_name
        self.host_name = configuration.client_host_name
        self.timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        self.data = []

    def add(self, sensor: str, measurement_type: str, measurement_unit: str, measurement_value: str,
            is_calculated: bool = False):
        if measurement_value is not None:
            self.data += [self.create(sensor, measurement_type, measurement_unit, measurement_value, is_calculated)]

    def create(self, sensor: str, measurement_type: str, measurement_unit: str, measurement_value: str,
               is_calculated: bool = False):
        return {
            "measurement": "data",
            "tags": {
                "host": self.host_name,
                "location": self.location,
                "type": measurement_type,
                "unit": measurement_unit,
                "sensor": sensor,
                "calculated": is_calculated
            },
            "time": self.timestamp,
            "fields": {
                "value": measurement_value
            }
        }
