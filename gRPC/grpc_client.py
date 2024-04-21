import grpc
import os
import sys
import socket
import uuid
import psutil
import threading
import time

from Interfaces.PrivateChatApp import PrivateChatApp

# Get the absolute path to the directory containing the module
module_dir = os.path.abspath("gRPC")
# Add the directory to the Python path
sys.path.append(module_dir)
import private_chat_pb2
import private_chat_pb2_grpc
from Redis.NameServer import NameServer


# Initialize NameServer instance
name_server = NameServer()


def get_listening_port(process_id):
    """Get the listening port of a process."""
    try:
        # Get the process by its ID
        process = psutil.Process(process_id)

        # Get the connections of the process
        connections = process.connections()

        # Filter connections that are listening
        listening_ports = [conn.laddr.port for conn in connections if conn.status == psutil.CONN_LISTEN]

        return listening_ports

    except psutil.NoSuchProcess:
        return None

# Function to find a free port
def find_free_port():
    # Create a socket and bind it to a random port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))  # Bind to localhost and a random port
        _, port = s.getsockname()  # Get the assigned port
    return port


class PrivateChatClient:
    def __init__(self, username):
        self.username = username
        self.client_id = str(uuid.uuid4())  # Generate a random UUID as the client ID
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.stub = None
        self.port = find_free_port()
        self.show_user_info()

    def connect_to_server(self):
        name_server.register_user(self.username, self.client_id, self.ip_address, self.port)
        try:
            # Connect to the server using the appropriate IP address and port
            channel = grpc.insecure_channel('127.0.0.1:50051')
            self.stub = private_chat_pb2_grpc.PrivateChatStub(channel)
        except Exception as e:
            # Display an error message if the connection fails
            print(f"Error connecting to server: {e}")

    def disconnect(self):
        name_server.remove_user(self.client_id)
        request = private_chat_pb2.DisconnectRequest(client_id=self.client_id)
        self.stub.Disconnect(request)
        print("Disconnected.")

    def send_message(self, message):
        if self.stub:
            try:
                self.stub.SendMessage(
                    private_chat_pb2.Message(sender_id=self.client_id, recipient_id=self.target_id, content=message))
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("Error: Not connected to server.")

    def receive_messages(self):
        while self.running:
            time.sleep(1)
            try:
                request = private_chat_pb2.ReceiveMessageRequest(
                    sender_id=self.target_id,
                    recipient_id=self.client_id
                )
                response = self.stub.ReceiveMessage(request)

                if response.HasField('message'):  # Check if the response contains a message
                    message = response.message
                    self.chat_ui.receive_message(message)
            except Exception as e:
                print(f"Error receiving messages: {e}")

    def show_user_info(self):
        print("Connected with ID: ", self.client_id)
        print("Connection info:\n"
              "\tIP address: ", self.ip_address,
              "\n\tPort: ", self.port)

    def start_chat(self):
        # Ask for the target
        self.target_id = input("Enter the target ID: ")
        connection_params = None

        while connection_params is None:
            connection_params = NameServer.get_connection_params(name_server, chat_id=self.target_id)
            if connection_params is None:
                print("User with ID '" + self.target_id + "' not found")
                self.target_id = input("Enter the target ID: ")

        self.target_ip = connection_params[b'ip_address'].decode()
        self.target_port = connection_params[b'port']
        self.target_username = connection_params[b'username'].decode()

        self.running = True
        self.listen_thread = threading.Thread(target=self.receive_messages)
        self.listen_thread.daemon = True  # Daemonize the thread so it exits when the main thread exits
        self.listen_thread.start()

        self.chat_ui = PrivateChatApp(self.username, self.target_username, self)
        self.chat_ui.mainloop()
        self.running = False