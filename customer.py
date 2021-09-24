

import pika
import json

from pika import channel
from pika import connection
from pika.spec import Queue

# for our connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('updateUser')
queue_name = queue.method.queue


channel.queue_bind(
    exchange='updateUser',
    queue=queue_name,
    routing_key='updateUser.update' # binding key
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print('[x] updating User {}'.format(payload['user_email']))
    print('[x] updated !')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)


print('[*] waiting for updating Customer ..')
channel.start_consuming()