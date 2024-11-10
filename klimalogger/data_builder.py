import time


class DataBuilder:
    def __init__(self):
        self.timestamp = time.time()
        self.data = []

    def add(self, sensor: str, measurement_type: str, measurement_unit: str, measurement_value: float,
            is_calculated: bool = False):
        if measurement_value is not None:
            self.data += [self.create(sensor, measurement_type, measurement_unit, measurement_value, is_calculated)]

    def create(self, sensor: str, measurement_type: str, measurement_unit: str, measurement_value: float,
               is_calculated: bool = False):
        return {
            "measurement": "data",
            "tags": {
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


def map_entry(mqtt_prefix, entry):
    timestamp = entry["time"]
    value = entry["fields"]["value"]
    tags = entry["tags"]
    measurement_type = tags["type"]
    unit = tags["unit"]
    sensor = tags["sensor"]
    topic = f"{mqtt_prefix}/{measurement_type}"
    print(f"{topic}: {value} {unit} ({sensor})")
    return (topic, {
        "time": timestamp,
        "value": value,
        "unit": unit,
        "sensor": sensor,
        "calculated": tags["calculated"]
    })
