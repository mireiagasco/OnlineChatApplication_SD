import functools
import subprocess
import socket
import threading
import time
import uuid
import atexit  # Module for registering cleanup functions
from colorama import init, Fore

from Interfaces.GroupChatApp import GroupChatApp
from RabbitMQ import RabbitMQbroker
from gRPC.grpc_client import PrivateChatClient
from Redis.NameServer import NameServer
from Interfaces.InsultChatApp import InsultChatApp


# Function to find a free port
def find_free_port():
    # Create a socket and bind it to a random port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))  # Bind to localhost and a random port
        _, port = s.getsockname()  # Get the assigned port
    return port


def private_chat(client_info):
    grpc_client = PrivateChatClient(client_info.username, client_info.client_id)
    grpc_client.connect_to_server()
    grpc_client.start_chat()


def connect_to_group_chat(client_info, spectator, persistent):
    group_chat_id = input("Enter the group chat id: ")
    app = GroupChatApp(client_info.username, client_info.client_id, group_chat_id, spectator, persistent)
    app.mainloop()


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
    RabbitMQbroker.send_discovery_message(client_info.client_id)
    time.sleep(2)


def test_redis():
    print("Testing Redis...")
    try:
        subprocess.run(["python", "TestServers/hello-world-redis.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running Redis test:", e)
    except FileNotFoundError:
        print("Error: Redis test file not found.")


def access_insult_channel(client_info):
    app = InsultChatApp(client_info.username, client_info.client_id)
    app.start()


def show_options(client_inst):
    while True:
        print("\n" + Fore.CYAN + "Options:" + Fore.RESET)
        print("1. " + Fore.MAGENTA + "Connect to chat" + Fore.RESET)
        print("2. " + Fore.MAGENTA + "Subscribe to group chat" + Fore.RESET)
        print("3. " + Fore.MAGENTA + "Discover chats" + Fore.RESET)
        print("4. " + Fore.MAGENTA + "Access insult channel" + Fore.RESET)
        print("5. " + Fore.MAGENTA + "Test REDIS" + Fore.RESET)
        print("6. " + Fore.RED + "Exit" + Fore.RESET)

        choice = input(Fore.YELLOW + "Enter your choice: " + Fore.RESET)

        if choice == "1":
            private_chat(client_inst)
        elif choice == "2":
            print("\n" + Fore.CYAN + "Options:" + Fore.RESET)
            print("1. " + Fore.MAGENTA + "Subscribe to group chat (receive)" + Fore.RESET)
            print("2. " + Fore.MAGENTA + "Connect to group chat (receive + send)" + Fore.RESET)
            option = input(Fore.YELLOW + "Enter your choice: " + Fore.RESET)
            print("\n" + Fore.CYAN + "Type of chat:" + Fore.RESET)
            print("1. " + Fore.MAGENTA + "Transient" + Fore.RESET)
            print("2. " + Fore.MAGENTA + "Persistent" + Fore.RESET)
            option2 = input(Fore.YELLOW + "Enter your choice: " + Fore.RESET)
            if option == "1":
                if option2 == "1":
                    connect_to_group_chat(client_inst, spectator=True, persistent=False)
                elif option2 == "2":
                    connect_to_group_chat(client_inst, spectator=True, persistent=True)
            elif option == "2":
                if option2 == "1":
                    connect_to_group_chat(client_inst, spectator=False, persistent=False)
                elif option2 == "2":
                    connect_to_group_chat(client_inst, spectator=False, persistent=True)
        elif choice == "3":
            print("\n" + Fore.CYAN + "Discovery Options:" + Fore.RESET)
            print("1. " + Fore.MAGENTA + "Discover chats via Redis" + Fore.RESET)
            print("2. " + Fore.MAGENTA + "Discover chats via RabbitMQ" + Fore.RESET)
            print("3. " + Fore.RED + "Back" + Fore.RESET)

            choice = input(Fore.YELLOW + "Enter your choice: " + Fore.RESET)

            if choice == "1":
                discover_chats_redis()
            elif choice == "2":
                discover_chats_rabbitmq(client_inst)
        elif choice == "4":
            access_insult_channel(client_inst)
        elif choice == "5":
            test_redis()
        elif choice == "6":
            print(Fore.RED + "Goodbye!" + Fore.RESET)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)


class Client:
    def __init__(self):
        self.username = None
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = find_free_port()
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

    def cleanup(self):
        # Remove user data from Redis
        name_server = NameServer()
        name_server.remove_user(self.client_id)
        print("User data removed from Redis.")

    def listen_for_discovery_messages(self):
        info = [self.client_id, self.username, self.ip_address, self.port]
        partial_callback = functools.partial(RabbitMQbroker.handle_discovery_message, client_info=info)
        RabbitMQbroker.receive_messages(exchange_name='chat_discovery', queue_name="discovery_queue",
                                        callback=lambda ch, method, properties, body: partial_callback(ch, method, properties, body, client_info=info))

    def listen_for_private_messages(self):
        RabbitMQbroker.receive_messages(exchange_name='direct_exchange', queue_name=self.client_id,
                                        callback=RabbitMQbroker.handle_private_message)

    def start(self):
        print("Welcome, {}!".format(self.username))
        show_options(self)


if __name__ == "__main__":
    client = Client()
    client.start()
