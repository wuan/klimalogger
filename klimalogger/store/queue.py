import json
import logging
import secrets
import time
from typing import List

from injector import inject
from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion

from .client import StoreClient
from .. import config

log = logging.getLogger(__name__)


class QueueStore(StoreClient):
    @inject
    def __init__(self, configuration: config.Config):
        self.qos = configuration.queue_qos
        self.mqtt_prefix = configuration.queue_prefix

        client_id = f'klimalogger-mqtt-{configuration.client_host_name}-{secrets.randbelow(1000)}'

        def on_connect(client, userdata, flags, reason_code, properties):
            if reason_code == 0:
                log.debug("Connected to MQTT Broker!")
            else:
                log.error("Failed to connect, return code %d", reason_code)

        def on_disconnect(client, userdata, rc):
            log.warning("Disconnected from MQTT Broker: %d", rc)

            delay = 5
            max_delay = 60

            while True:
                try:
                    if not client.reconnect():
                        log.info("Successful reconnect to MQTT Broker")
                        break
                except ConnectionRefusedError:
                    log.info("Reconnect to MQTT Broker failed, retry in %d seconds", delay)

                if delay < max_delay:
                    delay *= 2 + secrets.randbelow(5)

                time.sleep(delay)

        try:
            self.client = mqtt_client.Client(client_id=client_id, clean_session=False, callback_api_version = CallbackAPIVersion.VERSION2)
            # client.username_pw_set(username, password)
            self.client.on_connect = on_connect
            self.client.on_disconnect = on_disconnect
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

            if not self.client.is_connected():
                log.warning("client not connected, try to reconnect")
                self.client.reconnect()

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
