#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pika

credentials = pika.PlainCredentials('klima', 'klima')
connection = pika.BlockingConnection(pika.ConnectionParameters('queue', credentials=credentials, virtual_host='klima'))

channel = connection.channel()

channel.confirm_delivery()
properties = pika.BasicProperties(content_type='application/json', content_encoding="utf-8",
                                  type='measurement')
publish = channel.basic_publish(exchange='', routing_key='measurement', body='{"content": "Hello World!"}', properties=properties)
print(" [x] Sent 'Hello World!'")

connection.close()
