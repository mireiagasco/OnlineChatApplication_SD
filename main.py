import subprocess

from colorama import init, Fore
from gRPC.grpc_client import PrivateChatClient
from Redis.NameServer import NameServer


def private_chat(username):
    grpc_client = PrivateChatClient(username)
    grpc_client.connect_to_server()
    grpc_client.start_chat()


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

def show_options(username):
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
            private_chat(username)
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
        show_options(self.username)


if __name__ == "__main__":
    client = Client()
    name_server = NameServer()
    client.start()
