import json
import logging
import secrets
from typing import List

from injector import inject
from paho.mqtt import client as mqtt_client

from .client import StoreClient
from .. import config

log = logging.getLogger(__name__)


class QueueStore(StoreClient):
    @inject
    def __init__(self, configuration: config.Config):
        self.qos = configuration.queue_qos
        self.mqtt_prefix = configuration.queue_prefix

        client_id = f'klimalogger-mqtt-{configuration.client_host_name}-{secrets.randbelow(1000)}'

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                log.debug("Connected to MQTT Broker!")
            else:
                log.error("Failed to connect, return code %d", rc)

        try:
            self.client = mqtt_client.Client(client_id)
            # client.username_pw_set(username, password)
            self.client.on_connect = on_connect
            log.info("connect to host %s, port %d", configuration.service_host, configuration.service_port)
            self.client.connect(configuration.service_host, configuration.service_port)
            self.client.loop_start()
        except Exception:
            log.exception("could not create client")
            self.client = None

    def __del__(self):
        if self.client:
            self.client.disconnect()

    def store(self, data: List[dict]):
        if self.client:
            topic = "klimalogger"
            for entry in data:
                topic, json_message = self.map_entry(entry)
                message = json.dumps(json_message)
                log.info("write data (%d bytes) to topic %s", len(message), topic)
                result = self.client.publish(topic, payload=message, qos=self.qos, )
                status = result[0]
                if status != 0:
                    log.warning("Failed to send message to topic %s with status %s", topic, status)
        else:
            log.warning("client not available")
            raise RuntimeError("bla")

    def map_entry(self, entry: dict):
        timestamp = entry["time"]
        value = entry["fields"]["value"]
        tags = entry["tags"]
        measurement_type = tags["type"]
        unit = tags["unit"]
        sensor = tags["sensor"]
        topic = f"{self.mqtt_prefix}/{measurement_type}"
        print(f"{topic}: {value} {unit} ({sensor})")
        return (topic, {
            "time": int(timestamp),
            "value": value,
            "unit": unit,
            "sensor": sensor,
            "calculated": tags["calculated"]
        })
