import grpc
import os
import sys
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



class PrivateChatClient:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id
        self.stub = None
        self.show_user_info()

    def connect_to_server(self):
        try:
            # Connect to the server using the appropriate IP address and port
            channel = grpc.insecure_channel('127.0.0.1:50051')
            self.stub = private_chat_pb2_grpc.PrivateChatStub(channel)
            connect_request = private_chat_pb2.ConnectRequest(client_id=self.user_id)
            self.stub.Connect(connect_request)
        except Exception as e:
            # Display an error message if the connection fails
            print(f"Error connecting to server: {e}")

    def disconnect(self):
        request = private_chat_pb2.DisconnectRequest(client_id=self.user_id)
        self.stub.Disconnect(request)

    def send_message(self, message):
        if self.stub:
            try:
                self.stub.SendMessage(
                    private_chat_pb2.Message(sender_id=self.user_id, recipient_id=self.target_id, content=message))
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
                    recipient_id=self.user_id
                )
                response = self.stub.ReceiveMessage(request)

                if response.HasField('message'):  # Check if the response contains a message
                    message = response.message
                    self.chat_ui.receive_message(message)
                if response.HasField('disconnect_message'):  # If we receive a disconnectMessage
                    self.chat_ui.receive_message(disconnect=True)

            except Exception as e:
                print(f"Error receiving messages: {e}")

    def show_user_info(self):
        print("Connected with ID: ", self.user_id)

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