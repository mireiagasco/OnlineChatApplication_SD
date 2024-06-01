import functools
import socket
import threading
import time
import uuid
import atexit  # Module for registering cleanup functions
from colorama import init, Fore

import UserInteraction
from Interfaces.GroupChatApp import GroupChatApp
from RabbitMQ.RabbitMQBroker import RabbitMQBroker
from gRPC.grpc_client import PrivateChatClient
from Redis.NameServer import NameServer
from Interfaces.InsultChatApp import InsultChatApp


def private_chat(client_info):
    grpc_client = PrivateChatClient(client_info.username, client_info.client_id)
    grpc_client.connect_to_server()
    grpc_client.start_chat()


def connect_to_group_chat(client_info):
    spectator, persistent = UserInteraction.get_chat_options()
    group_chat_id = input("Enter the group chat id: ")
    app = GroupChatApp(client_info.username, client_info.client_id, group_chat_id, spectator, persistent)
    app.mainloop()


def chat_discovery(client_info):
    choice = UserInteraction.get_discovery_option()

    if choice == "1":
        discover_chats_redis()
    elif choice == "2":
        discover_chats_rabbitmq(client_info)


def discover_chats_redis():
    try:
        # Access the Redis NameServer singleton instance
        name_server = NameServer()

        # Get connected clients
        connected_clients = name_server.get_connected_clients()
        print("Discovering chats via Redis NameServer...")
        print("Connected clients:")
        for client_id, username in connected_clients.items():
            print("Client ID:", client_id, "Username:", username)
        print("Discovery complete!")

    except Exception as e:
        print("Error accessing Redis NameServer:", e)


def discover_chats_rabbitmq(client_info):
    print("Discovering chats via RabbitMQ...")
    RabbitMQBroker.send_discovery_message(client_info.client_id)
    time.sleep(2)
    print("Discovery complete!")


def access_insult_channel(client_info):
    app = InsultChatApp(client_info.username, client_info.client_id)
    app.start()


def show_options(client_inst):
    options = {
        "1": private_chat,
        "2": connect_to_group_chat,
        "3": chat_discovery,
        "4": access_insult_channel
    }

    while True:
        choice = UserInteraction.get_main_choice()
        if choice in options:
            options[choice](client_inst)
        elif choice == "5":
            print(Fore.RED + "Goodbye!" + Fore.RESET)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)


class Client:
    def __init__(self):
        self.username = None
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = self.find_free_port()
        self.client_id = str(uuid.uuid4())  # Generate a random UUID as the client ID
        init()  # Initialize colorama

        # Ask username
        print(Fore.GREEN + "Welcome to the Chat Client!" + Fore.RESET)
        self.username = input(Fore.YELLOW + "Enter your username: " + Fore.RESET)
        name_server = NameServer()
        name_server.register_user(self.username, self.client_id, self.ip_address, self.port)

        # Register cleanup function to remove user data from Redis when the program exits
        atexit.register(self.cleanup)

        # Start listening for messages
        threading.Thread(target=self.listen_for_discovery_messages, daemon=True).start()
        threading.Thread(target=self.listen_for_private_messages, daemon=True).start()

    # Function to find a free port
    @staticmethod
    def find_free_port():
        # Create a socket and bind it to a random port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))  # Bind to localhost and a random port
            _, port = s.getsockname()  # Get the assigned port
        return port

    def cleanup(self):
        # Remove user data from Redis
        name_server = NameServer()
        name_server.remove_user(self.client_id)

        # Remove RabbitMQ queue
        RabbitMQBroker.remove_queue(self.client_id)
        RabbitMQBroker.remove_queue(f"discovery_{self.client_id}")

    def listen_for_discovery_messages(self):
        info = [self.client_id, self.username, self.ip_address, self.port]
        partial_callback = functools.partial(RabbitMQBroker.handle_discovery_message, client_info=info)
        RabbitMQBroker.receive_messages(exchange_name='chat_discovery', queue_name=f"discovery_{self.client_id}",
                                        routing_key='discovery', callback=lambda ch, method, properties,
                                        body: partial_callback(ch, method, properties, body, client_info=info))

    def listen_for_private_messages(self):
        RabbitMQBroker.receive_messages(exchange_name='direct_exchange', queue_name=self.client_id,
                                        routing_key=self.client_id, callback=RabbitMQBroker.handle_private_message)

    def start(self):
        print("Welcome, {}!".format(self.username))
        show_options(self)


if __name__ == "__main__":
    RabbitMQBroker()
    client = Client()
    client.start()
