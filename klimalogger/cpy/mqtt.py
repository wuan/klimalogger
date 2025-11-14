import adafruit_minimqtt.adafruit_minimqtt as MQTT
from socketpool import SocketPool

from .. import Config


def connect(mqtt_client, userdata, flags, rc):
    print(f"  Connected to MQTT Broker. flags {flags}, RC: {rc}")


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("  Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print(f"  Subscribed to {topic} with QOS level {granted_qos}")


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print(f"  Unsubscribed from {topic} with PID {pid}")


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print(f"  Published to {topic} with PID {pid}")


def message(client, topic, message):
    print(f"  New message on topic {topic}: {message}")


class MQTTClient:

    def __init__(self, pool: SocketPool, config: Config):
        self.mqtt_client = MQTT.MQTT(
            broker=config.mqtt_host,
            port=config.mqtt_port,
            client_id=config.host_name,
            socket_pool=pool,
            is_ssl=False,
        )

        # Connect callback handlers to mqtt_client
        self.mqtt_client.on_connect = connect
        self.mqtt_client.on_disconnect = disconnect
        self.mqtt_client.on_subscribe = subscribe
        self.mqtt_client.on_unsubscribe = unsubscribe
        self.mqtt_client.on_message = message

    def publish(self, topic: str, message: str):
        try:
            self.mqtt_client.publish(topic, message, qos=1, retain=False)
        except OSError as e:
            print("Exception:", type(e), e)
            try:
                reconnect = self.mqtt_client.reconnect(False)
                print(f"Reconnecting to MQTT: {reconnect}")
            except Exception:
                pass
        except MQTT.MMQTTException as e:
            print("Exception:", type(e), e)

    def connect(self):
        self.mqtt_client.connect()
