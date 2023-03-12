#!/usr/bin/env python3

import secrets
import sys

from paho.mqtt import client as mqtt_client


def connect_mqtt(broker: str):
    port = 1883
    client_id = f'python-mqtt-{secrets.randbelow(1000)}'

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic: str):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def main():
    topic = "klimalogger"

    broker = sys.argv[1]
    client = connect_mqtt(broker)
    subscribe(client, topic)
    client.loop_forever()

if __name__ == "__main__":
    main()
