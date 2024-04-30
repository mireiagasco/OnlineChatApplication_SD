import tkinter as tk
from tkinter import scrolledtext
import threading
import pika
import json

# Connection parameters for RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
EXCHANGE_NAME = 'group_chats'


def send_message_to_chat(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
    channel = connection.channel()

    # Declare the exchange as a fanout exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

    # Publish the message to the fanout exchange
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='', body=json.dumps(message))

    connection.close()


class GroupChatApp(tk.Tk):
    def __init__(self, username, client_id, chat_id, spectator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = None
        self.stop_event = threading.Event()

        self.title(f"Group Chat {chat_id} - User: {username}")
        self.username = username
        self.chat_id = chat_id
        self.spectator = spectator

        # Create scrolled text widget to display messages
        self.chat_history = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.chat_history.pack(expand=True, fill=tk.BOTH)

        # Create entry widget to type messages
        self.message_entry = tk.Entry(self)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Disable message entry for spectators
        self.message_entry.configure(state='disabled' if spectator else 'normal')

        # Create send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        self.send_button.configure(state='disabled' if spectator else 'normal')  # Disable send button for spectators

        # Apply formatting to tags
        self.chat_history.tag_config("sent", justify="right")
        self.chat_history.tag_config("received", justify="left")

        # Start receiving messages
        self.receive_messages(client_id=client_id)

        # Ensure threads stop when the window is closed
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.stop_event.set()
        self.destroy()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(f"{self.username}: {message}", status='sent')
            send_message_to_chat({'sender': self.username, 'content': message})
            self.message_entry.delete(0, tk.END)

    def receive_messages(self, client_id):
        queue_name = f"chat_{self.chat_id}_{client_id}"

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
        channel = connection.channel()

        # Declare the exchange as a fanout exchange
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')

        # Declare the queue and bind it to the exchange
        result = channel.queue_declare(queue=queue_name, exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

        def callback(ch, method, properties, body):
            message = json.loads(body)
            sender = message.get('sender')
            if sender != self.username:  # Ignore messages sent by yourself
                self.display_message(f"{message['sender']}: {message['content']}", status='received')

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.thread = threading.Thread(target=self.consume_messages, args=(channel,), daemon=True)
        self.thread.start()

    def consume_messages(self, channel):
        try:
            # Start consuming messages
            while not self.stop_event.is_set():
                channel.connection.process_data_events(time_limit=1)
        except Exception as e:
            print(f"Error consuming messages: {e}")
        finally:
            # Close the channel and connection
            channel.close()

    def display_message(self, message, status):
        tag = None

        if status == 'sent':
            tag = "sent"
        if status == 'received':
            tag = "received"

        # Insert the message with the corresponding tag
        self.chat_history.insert(tk.END, message + '\n', tag)
        self.chat_history.see(tk.END)
