import pika
import json

from pika import channel


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_report')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.report' # binding key
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print('[x] Generating Report ... ')
    print(f"""
    ID: {payload.get('id')}
    User Email: {payload.get('user_email')}
    Product: {payload.get('prodcut')}
    Quantity: {payload.get('quantity')} 
    """)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)


print('[*] waiting for sending Report ...')
channel.start_consuming()