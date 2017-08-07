import json

import pika
from injector import inject

from .. import config
from .client import StoreClient


class QueueStore(StoreClient):
    @inject
    def __init__(self, configuration : config.Config):
        try:
            credentials = pika.PlainCredentials(configuration.queue_username, configuration.queue_password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=configuration.queue_host,
                port=configuration.queue_port,
                virtual_host=configuration.queue_virtual_host,
                credentials=credentials
            ))
        except Exception as e:
            print("could not create client", e)
            self.connection = None

    def __del__(self):
        if self.connection:
            self.connection.close()

    def store(self, data: dict):
        if self.connection:

            print("write data")
            channel = self.connection.channel()
            channel.confirm_delivery()

            delivery_confirmed = channel.basic_publish(exchange='', routing_key='measurement', body=json.dumps(data),
                                                       mandatory=True)

            if not delivery_confirmed:
                print("message was not confirmed")
                raise RuntimeError("message was not confirmed")

        else:
            print("client not available")
            raise RuntimeError("bla")
