# RabbitMQBroker.py

import pika
import json
import threading

# Connection parameters
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
EXCHANGE_NAME_CHAT = 'group_chats'
EXCHANGE_NAME_DISCOVERY = 'chat_discovery'
DISCOVERY_QUEUE_NAME = 'discovery_queue'
EXCHANGE_NAME_DIRECT = 'direct_exchange'

# Function to send a message to the RabbitMQ exchange
def send_message(exchange_name, routing_key, message, persistent=False):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
    channel = connection.channel()
    properties = pika.BasicProperties(delivery_mode=2 if persistent else 1)  # 2 for persistent, 1 for transient

    if exchange_name == EXCHANGE_NAME_DIRECT:
        channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=persistent)
    else:
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=persistent)

    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(message), properties=properties)
    connection.close()


# Function to receive messages from the RabbitMQ queue
def receive_messages(exchange_name, queue_name, callback, persistent=False):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type='direct' if exchange_name == EXCHANGE_NAME_DIRECT else 'fanout', durable=persistent)
    result = channel.queue_declare(queue=queue_name, durable=persistent)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    # Set up the callback function to process messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Start a new thread to consume messages
    threading.Thread(target=channel.start_consuming, args=(), daemon=True).start()


# Function to send a discovery message to the RabbitMQ exchange
def send_discovery_message(message):
    send_message(EXCHANGE_NAME_DISCOVERY, DISCOVERY_QUEUE_NAME, message)


# Function to handle discovery message
def handle_discovery_message(ch, method, properties, body, client_info):
    # Prepare the response message with client's information
    response_message = {
        'client_id': client_info[0],
        'username': client_info[1],
        'ip_address': client_info[2],
        'port': client_info[3]
    }
    key = body.decode().strip('"')
    # Send the response message directly to the sender
    send_message(exchange_name=EXCHANGE_NAME_DIRECT, routing_key=key, message=response_message)

def handle_private_message(ch, method, properties, body):
    print("Received private message:", body.decode())

def send_insult(insult_message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=insult_message,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ))
    connection.close()

def receive_insult(insults_queue, condition):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    def callback(ch, method, properties, body):
        with condition:
            insults_queue.put(body.decode())
            condition.notify_all()  # Notify all waiting threads        time.sleep(body.count(b'.'))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


def remove_queue(queue_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_delete(queue=queue_name)