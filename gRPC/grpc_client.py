import grpc
import os
import sys
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
    def __init__(self, username, target_id, target_username):
        self.client_id = target_id
        self.username = username
        self.target_username = target_username
        self.stub = None
        self.chat_ui = PrivateChatApp(self.username, target_username, self)
        self.chat_ui.mainloop()
        self.connect_to_server(target_id, target_username)

    def connect_to_server(self, ip_address, port):
        channel = grpc.insecure_channel(f"{ip_address}:{port}")
        self.stub = private_chat_pb2_grpc.PrivateChatStub(channel)
        response = self.stub.Connect(private_chat_pb2.ConnectRequest(client_id=self.client_id))
        self.chat_ui.display_message(response.message)

    def send_message(self, message):
        if self.stub:
            self.stub.SendMessage(private_chat_pb2.Message(sender=self.client_id, content=message))
        else:
            self.chat_ui.display_message("Error: Not connected to server.")
    def receive_messages(self):
        while True:
            try:
                response = self.stub.ReceiveMessage(private_chat_pb2.Empty())
                # Display the received message in the UI
                self.chat_ui.receive_message(f"{response.sender_id}: {response.content}")
            except Exception as e:
                self.chat_ui.display_message(f"Error receiving message: {e}")
                break




