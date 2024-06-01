# RabbitMQBroker.py

import pika
import json
import threading


class RabbitMQBroker:
    # Connection parameters
    RABBITMQ_HOST = 'localhost'
    RABBITMQ_PORT = 5672
    RABBITMQ_USERNAME = 'guest'
    RABBITMQ_PASSWORD = 'guest'
    EXCHANGE_NAME_CHAT_T = 'group_chats_t'
    EXCHANGE_NAME_CHAT_P = 'group_chats_p'
    EXCHANGE_NAME_DISCOVERY = 'chat_discovery'
    DISCOVERY_QUEUE_NAME = 'discovery_queue'
    EXCHANGE_NAME_DIRECT = 'direct_exchange'
    HISTORY_EXCHANGE = '_history'

    @staticmethod
    # Function to send a message to the RabbitMQ exchange
    def send_message(exchange_name, routing_key, message, persistent=False):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RabbitMQBroker.RABBITMQ_HOST, port=RabbitMQBroker.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RabbitMQBroker.RABBITMQ_USERNAME, RabbitMQBroker.RABBITMQ_PASSWORD)))
        channel = connection.channel()
        properties = pika.BasicProperties(delivery_mode=2 if persistent else 1)  # 2 for persistent, 1 for transient

        # Determine the exchange type
        exchange_type = 'direct' if exchange_name in [RabbitMQBroker.EXCHANGE_NAME_DIRECT,
                                                      RabbitMQBroker.EXCHANGE_NAME_CHAT_T,
                                                      RabbitMQBroker.EXCHANGE_NAME_CHAT_P,
                                                      RabbitMQBroker.HISTORY_EXCHANGE] else 'fanout'

        # Publish to the main exchange
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=persistent)
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key,
                              body=json.dumps(message), properties=properties)

        if persistent:
            # Declare and publish to the history exchange
            history_exchange_name = exchange_name + RabbitMQBroker.HISTORY_EXCHANGE
            channel.exchange_declare(exchange=history_exchange_name, exchange_type='fanout', durable=True)
            channel.basic_publish(exchange=history_exchange_name, routing_key=routing_key,
                                  body=json.dumps(message), properties=properties)

        connection.close()

    @staticmethod
    # Function to receive messages from the RabbitMQ queue
    def receive_messages(exchange_name, queue_name, routing_key, callback, persistent=False):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RabbitMQBroker.RABBITMQ_HOST, port=RabbitMQBroker.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RabbitMQBroker.RABBITMQ_USERNAME, RabbitMQBroker.RABBITMQ_PASSWORD)))
        channel = connection.channel()

        # Determine the exchange type
        exchange_type = 'direct' if exchange_name in [RabbitMQBroker.EXCHANGE_NAME_DIRECT,
                                                      RabbitMQBroker.EXCHANGE_NAME_CHAT_T,
                                                      RabbitMQBroker.EXCHANGE_NAME_CHAT_P,
                                                      RabbitMQBroker.HISTORY_EXCHANGE] else 'fanout'

        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=persistent)
        result = channel.queue_declare(queue=queue_name, durable=persistent)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

        if persistent:
            # Retrieve messages from the history queue
            history_exchange_name = exchange_name + RabbitMQBroker.HISTORY_EXCHANGE
            history_queue_name = 'history_' + exchange_name
            channel.exchange_declare(exchange=history_exchange_name, exchange_type='fanout', durable=True)
            channel.queue_declare(queue=history_queue_name, durable=True)
            channel.queue_bind(exchange=history_exchange_name, queue=history_queue_name)

            def load_history_messages():
                messages = []  # Store messages temporarily
                while True:
                    method_frame, properties, body = channel.basic_get(history_queue_name, auto_ack=False)
                    if method_frame:
                        message = json.loads(body)
                        message_key = method_frame.routing_key
                        if routing_key == message_key:
                            channel.basic_publish(exchange='',
                                                  routing_key=queue_name,
                                                  body=json.dumps(message),
                                                  properties=properties)
                        # Acknowledge the message
                        messages.append((body, properties, message_key))
                        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    else:
                        break

                # Republish messages in the same order
                for body, properties, message_key in messages:
                    channel.basic_publish(exchange=history_exchange_name,
                                          routing_key=message_key,
                                          body=body,
                                          properties=properties)
                # Re-bind the history queue to the history exchange with the correct routing key
                channel.queue_bind(exchange=history_exchange_name, queue=history_queue_name)

            load_history_messages()

        # Set up the callback function to process messages
        def on_message_callback(ch, method, properties, body):
            callback(ch, method, properties, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=False)

        # Start a new thread to consume messages
        threading.Thread(target=channel.start_consuming, args=(), daemon=True).start()

    @staticmethod
    # Function to send a discovery message to the RabbitMQ exchange
    def send_discovery_message(message):
        RabbitMQBroker.send_message(exchange_name=RabbitMQBroker.EXCHANGE_NAME_DISCOVERY,
                                    routing_key='discovery', message=message)

    @staticmethod
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
        RabbitMQBroker.send_message(exchange_name=RabbitMQBroker.EXCHANGE_NAME_DIRECT,
                                    routing_key=key, message=response_message)

    @staticmethod
    def handle_private_message(ch, method, properties, body):
        print("Received private message:", body.decode())

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def remove_queue(queue_name):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_delete(queue=queue_name)
