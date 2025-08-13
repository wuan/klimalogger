#!/usr/bin/env python3

import secrets
import sys

import paho.mqtt.client as mqtt_client


def connect_mqtt(broker: str):
    port = 1883
    client_id = f"python-mqtt-{secrets.randbelow(1000)}"

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", reason_code)

    # Set Connecting Client ID
    client = mqtt_client.Client(
        client_id=client_id,
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
    )
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client.Client, topic: str):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def main():
    topic = "sensors/#"

    broker = sys.argv[1]
    client = connect_mqtt(broker)
    subscribe(client, topic)
    client.loop_forever()


if __name__ == "__main__":
    main()
