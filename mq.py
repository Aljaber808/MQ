import  pika 
import json
import uuid

from pika import channel
from pika import exchange_type
from pika.spec import Queue

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='order',
    exchange_type='direct'
)

channel.exchange_declare(
    exchange='updateUser',
    exchange_type='direct'
)


order = {
    'id': str(uuid.uuid4()),
    'user_email': 'user_email@email.com',
    'product': 'Laptop',
    'quantity': 1
}


customer = {
    'id': str(uuid.uuid4()),
    'usere_email': 'user_email@email.com',
    'User Name': 'User1',
    'User Age': 30
}

channel.basic_publish(
    exchange='updateUser',
    routing_key = 'updateUser.update',
    body=json.dumps({'user_email': customer['usere_email']})
)
print('[x] Updated Custmer')

channel.basic_publish(
    exchange='order',
    routing_key = 'order.notify',
    body=json.dumps({'user_email': order['user_email']})
)
print('[x] Sent notify meesage')

channel.basic_publish(
    exchange='order',
    routing_key='order.report',
    body=json.dumps(order)
)
print('[x] Sent Report Message')

connection.close