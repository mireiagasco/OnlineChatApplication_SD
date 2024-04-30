import subprocess
import socket
import uuid
import json

from colorama import init, Fore

from Interfaces.GroupChatApp import GroupChatApp
from gRPC.grpc_client import PrivateChatClient
from Redis.NameServer import NameServer


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

def connect_to_group_chat(client_info, spectator):
    group_chat_id = input("Enter the group chat id: ")
    app = GroupChatApp(client_info.username, client_info.client_id, group_chat_id, spectator)
    app.mainloop()


def discover_chats():
    print("Discovering chats...")
    # Placeholder for discovering chats logic


def test_redis():
    print("Testing Redis...")
    try:
        subprocess.run(["python", "TestServers/hello-world-redis.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running Redis test:", e)
    except FileNotFoundError:
        print("Error: Redis test file not found.")


def access_insult_channel():
    print("Accessing insult channel...")
    # Placeholder for accessing insult channel logic


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
            if option == "1":
                connect_to_group_chat(client_inst, spectator=True)
            elif option == "2":
                connect_to_group_chat(client_inst, spectator=False)

        elif choice == "3":
            discover_chats()
        elif choice == "4":
            access_insult_channel()
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

    def start(self):
        print(Fore.GREEN + "Welcome to the Chat Client!" + Fore.RESET)
        self.username = input(Fore.YELLOW + "Enter your username: " + Fore.RESET)
        name_server.register_user(self.username, self.client_id, self.ip_address, self.port)
        print("Welcome, {}!".format(self.username))
        show_options(self)


if __name__ == "__main__":
    client = Client()
    name_server = NameServer()
    client.start()
