import tkinter as tk
from tkinter import scrolledtext
import threading
import json

from RabbitMQ.RabbitMQBroker import RabbitMQBroker


# Connection parameters for RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
EXCHANGE_NAME = 'group_chats'


class GroupChatApp(tk.Tk):
    def __init__(self, username, client_id, chat_id, spectator, persistent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = None
        self.stop_event = threading.Event()

        self.title(f"Group Chat {chat_id} - User: {username}")
        self.username = username
        self.chat_id = chat_id
        self.client_id = client_id
        self.spectator = spectator
        self.persistent = persistent

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
        self.receive_messages(client_id=client_id, persistent=self.persistent)

        # Ensure threads stop when the window is closed
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.stop_event.set()
        queue_name = f"chat_{self.chat_id}_{self.client_id}_{'persistent' if self.persistent else 'transient'}"
        RabbitMQBroker.remove_queue(queue_name)
        self.destroy()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(f"{self.username}: {message}", status='sent')
            routing_key = f"chat_{self.chat_id}_{'persistent' if self.persistent else 'transient'}"
            RabbitMQBroker.send_message(EXCHANGE_NAME, routing_key=routing_key,
                                        message={'sender': self.username, 'content': message},
                                        persistent=self.persistent)
            self.message_entry.delete(0, tk.END)

    def receive_messages(self, client_id, persistent):
        queue_name = f"chat_{self.chat_id}_{client_id}_{'persistent' if persistent else 'transient'}"
        routing_key = f"chat_{self.chat_id}_{'persistent' if persistent else 'transient'}"
        RabbitMQBroker.receive_messages(exchange_name='group_chats', queue_name=queue_name, routing_key=routing_key,
                                        callback=self.callback, persistent=persistent)

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        sender = message.get('sender')
        if sender != self.username:  # Ignore messages sent by yourself
            self.display_message(f"{message['sender']}: {message['content']}", status='received')

    def display_message(self, message, status):
        tag = None

        if status == 'sent':
            tag = "sent"
        if status == 'received':
            tag = "received"

        # Insert the message with the corresponding tag
        self.chat_history.insert(tk.END, message + '\n', tag)
        self.chat_history.see(tk.END)
