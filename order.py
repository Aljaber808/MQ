

import pika
import json

from pika import channel
from pika import connection
from pika.spec import Queue

# for our connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_notify')
queue_name = queue.method.queue


channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.notify' # binding key
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print('[x] Notifying {}'.format(payload['user_email']))
    print('[x] Done !')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)


print('[*] waiting for notfiy message')
channel.start_consuming()