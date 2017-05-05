import json

import pika
from injector import inject

from .. import config
from .client import StoreClient


class QueueStore(StoreClient):
    @inject(configuration=config.Config)
    def __init__(self, configuration):
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
            self.connection.channel() \
                .basic_publish(exchange='',
                               routing_key='measurement',
                               body=json.dumps(data))
        else:
            print("client not available")
            raise RuntimeError("bla")


def client():
    from . import INJECTOR

    return INJECTOR.get(StoreClient)
