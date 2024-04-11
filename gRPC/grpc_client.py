import grpc
import os
import sys
import socket
import uuid
# Get the absolute path to the directory containing the module
module_dir = os.path.abspath("gRPC")
# Add the directory to the Python path
sys.path.append(module_dir)
import private_chat_pb2
import private_chat_pb2_grpc
from Redis.NameServer import NameServer
from Interfaces.PrivateChatApp import PrivateChatApp

# Initialize NameServer instance
name_server = NameServer()

class PrivateChatClient:
    def __init__(self, username):
        self.username = username
        self.client_id = str(uuid.uuid4())  # Generate a random UUID as the client ID
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = 50051
        self.target_id = None
        self.showUserInfo()
        # Register user info
        name_server.register_user(username, self.client_id, self.ip_address, self.port)

        connection_params = self.getTarget()
        self.target_ip = connection_params[b'ip_address'].decode()
        self.target_port = connection_params[b'port']
        self.target_username = connection_params[b'username'].decode()

        self.chat_ui = PrivateChatApp(self.username, self.target_username, self)
        self.connect_to_server()  # Connect to the server when the client is initialized
        self.chat_ui.mainloop()

    def connect_to_server(self):
        try:
            # Connect to the server using the appropriate IP address and port
            channel = grpc.insecure_channel('127.0.0.1:50051')
            self.stub = private_chat_pb2_grpc.PrivateChatStub(channel)
            response = self.stub.Connect(private_chat_pb2.ConnectRequest(client_id=self.client_id))
            self.chat_ui.display_message(response.message)
        except Exception as e:
            # Display an error message if the connection fails
            self.chat_ui.display_message(f"Error connecting to server: {e}")

    def send_message(self, message):
        print("Sending message... (grpc client)")
        if self.stub:
            try:
                # Attempt to send the message only if the connection is established
                self.stub.SendMessage(private_chat_pb2.Message(sender=self.client_id, destination=self.target_id, content=message))
            except Exception as e:
                self.chat_ui.display_message(f"Error sending message: {e}")
        else:
            self.chat_ui.display_message("Error: Not connected to server.")

    def receive_messages(self):
        while True:
            try:
                response = self.stub.ReceiveMessage(private_chat_pb2.Empty())
                # Display the received message in the UI
                self.chat_ui.receive_message(f"{response.sender_id}: {response.content}")
            except Exception as e:
                # Display the error message, but continue receiving messages
                self.chat_ui.display_message(f"Error receiving message: {e}")

    def showUserInfo(self):
        print("Connected with ID: ", self.client_id)
        print("Connection info:\n"
              "\tIP address: ", self.ip_address,
              "\n\tPort: ", self.port)

    def getTarget(self):
        # Ask for the target
        self.target_id = input("Enter the target ID: ")
        connection_params = None

        while connection_params is None:
            connection_params = NameServer.get_connection_params(name_server, chat_id=self.target_id)
            if connection_params is None:
                print("User with ID '" + self.target_id + "' not found")
                target_id = input("Enter the target ID: ")

        return connection_params



