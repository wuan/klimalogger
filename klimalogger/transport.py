import json
import random

try:
    from paho.mqtt import client as mqtt_client
    from paho.mqtt.enums import CallbackAPIVersion
except ImportError:
    pass

# StoreClient removed; using concrete class
from . import config
from .logger import create_logger

log = create_logger(__name__)


class QueueTransport:
    def __init__(self, configuration: config.Config):
        self.qos = configuration.mqtt_qos
        self.mqtt_prefix = configuration.mqtt_prefix
        self.client: mqtt_client.Client | None = None

        client_id = (
            f"klimalogger-mqtt-{configuration.host_name}-{random.randrange(1,1000)}"
        )

        def on_connect(client, userdata, flags, reason_code, properties):
            if reason_code == 0:
                log.debug("Connected to MQTT Broker!")
            else:
                log.error("Failed to connect, return code %d", reason_code)

        def on_disconnect(client, userdata, flags, reason_code, properties):
            log.warning(f"Disconnected from MQTT Broker: {reason_code}")

        try:
            self.client = mqtt_client.Client(
                client_id=client_id,
                clean_session=False,
                callback_api_version=CallbackAPIVersion.VERSION2,
            )
            # client.username_pw_set(username, password)
            self.client.on_connect = on_connect
            self.client.on_disconnect = on_disconnect
            log.info(
                "connect to host %s, port %d",
                configuration.mqtt_host,
                configuration.mqtt_port,
            )
            self.client.connect(configuration.mqtt_host, configuration.mqtt_port)
            self.client.loop_start()
        except Exception:
            log.exception("could not create client")
            self.client = None

    def __del__(self):
        if self.client:
            self.client.disconnect()

    def store(self, data: list[dict]):
        if self.client:

            if not self.client.is_connected():
                log.warning("client not connected, try to reconnect")
                try:
                    self.client.reconnect()
                except Exception:
                    log.warning("reconnect failed")

            for entry in data:
                topic, json_message = map_entry(self.mqtt_prefix, entry)
                message = json.dumps(json_message)
                log.info("write data (%d bytes) to topic %s", len(message), topic)
                result = self.client.publish(
                    topic,
                    payload=message,
                    qos=self.qos,
                )
                status = result[0]
                if status != 0:
                    log.warning(
                        "Failed to send message to topic %s with status %s",
                        topic,
                        status,
                    )
        else:
            log.warning("client not available")
            raise RuntimeError("bla")


def map_entry(mqtt_prefix: str, entry: dict):
    timestamp = entry["time"]
    value = entry["fields"]["value"]
    tags = entry["tags"]
    measurement_type = tags["type"]
    unit = tags["unit"]
    sensor = tags["sensor"]
    topic = f"{mqtt_prefix}/{measurement_type}"
    return (
        topic,
        {
            "time": int(timestamp),
            "value": value,
            "unit": unit,
            "sensor": sensor,
            "calculated": tags["calculated"],
        },
    )
