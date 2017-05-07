#!/usr/bin/env python3
# -*- coding: utf8 -*-
import json

import pika

credentials = pika.PlainCredentials('klima', 'klima')
connection = pika.BlockingConnection(pika.ConnectionParameters('queue', credentials=credentials, virtual_host='klima'))

channel = connection.channel()

channel.queue_declare(queue='measurement', durable=True)

def callback(ch, method, properties, body):
    #import pdb;
    #pdb.set_trace()


    content_encoding = properties.content_encoding
    decoded_body = body.decode(content_encoding)

    content_type = properties.content_type
    if content_type == 'application/json':
        decoded_body = json.loads(decoded_body)

    print(" [x] Received %r" % (decoded_body))

channel.basic_consume(callback,
                      queue='measurement',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

