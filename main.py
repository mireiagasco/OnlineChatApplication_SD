import subprocess
from colorama import init, Fore
import grpc
import sys
import os

# Get the absolute path to the directory containing the module
module_dir = os.path.abspath("gRPC")
# Add the directory to the Python path
sys.path.append(module_dir)

from gRPC.private_chat_pb2_grpc import PrivateChatStub
from gRPC.private_chat_pb2 import ConnectRequest
from gRPC.grpc_client import connect_to_server

def private_chat():
    # Establish a gRPC channel
    grpc_channel = grpc.insecure_channel('localhost:50051')
    stub = PrivateChatStub(grpc_channel)

    # Connect to the server
    response = stub.Connect(ConnectRequest())

    # Display the assigned ID
    print(response.message)

    #Ask for the target
    target_id = input("Enter the target ID: ")
    connect_to_server(target_id)

def subscribe_to_group_chat(group_chat_id):
    print("Subscribing to group chat {}...".format(group_chat_id))
    # Placeholder for actual subscription logic


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

def show_options():
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
            private_chat()
        elif choice == "2":
            group_chat_id = input("Enter the group chat id: ")
            subscribe_to_group_chat(group_chat_id)
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
        init()  # Initialize colorama

    def start(self):
        print(Fore.GREEN + "Welcome to the Chat Client!" + Fore.RESET)
        self.username = input(Fore.YELLOW + "Enter your username: " + Fore.RESET)
        print("Welcome, {}!".format(self.username))
        show_options()


if __name__ == "__main__":
    client = Client()
    client.start()
