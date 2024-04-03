import grpc
import private_chat_pb2
import private_chat_pb2_grpc
from Redis.NameServer import NameServer

# Initialize NameServer instance
name_server = NameServer()

def connect_to_server(target_id):
    # Retrieve connection parameters associated with the target_id from the name server
    connection_params = name_server.get_connection_params(target_id)

    if connection_params:
        # Extract IP address and port from connection parameters
        ip_address = connection_params.get('ip_address')
        port = connection_params.get('port')

        # Establish gRPC channel
        channel = grpc.insecure_channel(f"{ip_address}:{port}")
        stub = private_chat_pb2_grpc.PrivateChatStub(channel)

        # Implement logic to handle response
        response = stub.Connect(private_chat_pb2.ConnectRequest())
        print(response.message)  # Handle the response message
    else:
        print("Chat not found or connection details not available.")

def send_message(target_id, sender, content):
    # Retrieve connection parameters associated with the target_id from the name server
    connection_params = name_server.get_connection_params(target_id)

    if connection_params:
        # Extract IP address and port from connection parameters
        ip_address = connection_params.get('ip_address')
        port = connection_params.get('port')

        # Establish gRPC channel
        channel = grpc.insecure_channel(f"{ip_address}:{port}")
        stub = private_chat_pb2_grpc.PrivateChatStub(channel)

        # Create message
        message = private_chat_pb2.Message(sender=sender, content=content)
        stub.SendMessage(message)
    else:
        print("Chat not found or connection details not available.")

def receive_message(target_id):
    # Retrieve connection parameters associated with the target_id from the name server
    connection_params = name_server.get_connection_params(target_id)

    if connection_params:
        # Extract IP address and port from connection parameters
        ip_address = connection_params.get('ip_address')
        port = connection_params.get('port')

        # Establish gRPC channel
        channel = grpc.insecure_channel(f"{ip_address}:{port}")
        stub = private_chat_pb2_grpc.PrivateChatStub(channel)

        # Receive message
        message = stub.ReceiveMessage(private_chat_pb2.Empty())
        print(f"Message from {message.sender}: {message.content}")
    else:
        print("Chat not found or connection details not available.")
