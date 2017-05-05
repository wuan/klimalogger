#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pika

credentials = pika.PlainCredentials('klima', 'klima')
connection = pika.BlockingConnection(pika.ConnectionParameters('nyx', credentials=credentials, virtual_host='klima'))

channel = connection.channel()

channel.basic_publish(exchange='',
                      routing_key='measurement',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
