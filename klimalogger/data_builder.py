import socket
import datetime
import pytz
from injector import singleton, inject
from . import config


@singleton
class DataBuilder(object):
    @inject(configuration=config.Config)
    def __init__(self, configuration):
        self.location = configuration.client_location_name
        self.host_name = socket.gethostname()
        self.timestamp = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        self.data = []

    def add(self, sensor, measurement_type, measurement_unit, measurement_value, calculated=False):
        if measurement_value is not None:
            self.data += [self.create(sensor, measurement_type, measurement_unit, measurement_value, calculated)]

    def create(self, sensor, measurement_type, measurement_unit, measurement_value, is_calculated=False):
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
