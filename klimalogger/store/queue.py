import json
import logging
import random

from injector import inject
from paho.mqtt import client as mqtt_client

from .client import StoreClient
from .influxdb import InfluxDbStore
from .. import config

log = logging.getLogger(__name__)


class CombinedStore(StoreClient):

    @inject
    def __init__(self, configuration: config.Config):
        log.info("create combined store")
        self.stores = [
            InfluxDbStore(configuration),
            QueueStore(configuration)
        ]

    def store(self, data):
        for store in self.stores:
            store.store(data)


class QueueStore(StoreClient):
    @inject
    def __init__(self, configuration: config.Config):

        client_id = f'klimalogger-mqtt-{configuration.client_host_name}-{random.randint(0, 1000)}'

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                log.debug("Connected to MQTT Broker!")
            else:
                log.error("Failed to connect, return code %d", rc)

        try:
            self.client = mqtt_client.Client(client_id)
            # client.username_pw_set(username, password)
            self.client.on_connect = on_connect
            log.info("connect to host %s, port %d", configuration.queue_host, configuration.queue_port)
            self.client.connect(configuration.queue_host, configuration.queue_port)
        except Exception:
            log.exception("could not create client")
            self.client = None

    def __del__(self):
        if self.client:
            self.client.disconnect()

    def store(self, data: dict):
        if self.client:
            topic = "klimalogger"
            for entry in data:
                json_message = {}
                json_message.update(entry["tags"])
                json_message["time"] = entry["time"]
                json_message.update(entry["fields"])
                message = json.dumps(json_message)
                log.info("write data (%d bytes) to topic %s", len(message), topic)
                result = self.client.publish(topic, message)
                status = result[0]
                if status != 0:
                    log.warning("Failed to send message to topic %s with status %s", topic, status)
        else:
            log.warning("client not available")
            raise RuntimeError("bla")
