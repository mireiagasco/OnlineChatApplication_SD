import pika
import json

# Connection parameters
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'


# Function to send a message to the RabbitMQ exchange
def send_message(exchange_name, routing_key, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    # Make message persistent by setting delivery_mode to 2
    properties = pika.BasicProperties(delivery_mode=2)

    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(message),
                          properties=properties)
    print(" [x] Sent %r:%r" % (routing_key, message))


    connection.close()


# Function to receive messages from the RabbitMQ queue
def receive_messages(queue_name, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Example callback function to process received messages
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# Example usage
if __name__ == '__main__':
    # Define exchange name and routing key
    EXCHANGE_NAME = 'chat_exchange'
    ROUTING_KEY = 'group_chat'

    # Send a message
    message = {'sender': 'user1', 'content': 'Hello, group!'}
    send_message(EXCHANGE_NAME, ROUTING_KEY, message)

    # Receive messages
    receive_messages(ROUTING_KEY, callback)
