import logging
import os
from datetime import datetime
from typing import List

from .client import StoreClient

log = logging.getLogger(__name__)


class FileStore(StoreClient):
    target_folder = "/var/lib/klimalogger/data"

    def store(self, data: List[dict]):
        for entry in data:
            timestamp = datetime.fromtimestamp(entry["time"])
            value = entry["fields"]["value"]
            tags = entry["tags"]
            measurement_type = tags["type"]
            unit = tags["unit"]
            sensor = tags["sensor"]
            folder_name = f"{self.target_folder}/{timestamp:%Y}/{timestamp:%m}/"
            file_name = f"{measurement_type}_{timestamp:%Y%m%d}.txt"

            os.makedirs(folder_name, exist_ok=True)
            with open(folder_name + '/' + file_name, 'a') as output_file:
                output_file.write(f"{timestamp.isoformat()} {value} {unit} {sensor}\n")
