#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pika

credentials = pika.PlainCredentials('klima', 'klima')
connection = pika.BlockingConnection(pika.ConnectionParameters('nyx', credentials=credentials, virtual_host='klima'))

channel = connection.channel()

channel.queue_declare(queue='measurement')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='measurement',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

