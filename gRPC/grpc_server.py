import grpc
from concurrent import futures
import private_chat_pb2
import private_chat_pb2_grpc
import uuid
from Redis.NameServer import NameServer
import socket


name_server = NameServer()


class PrivateChatService(private_chat_pb2_grpc.PrivateChatServicer):
    def __init__(self):
        self.connections = {}  # Dictionary to store client connections

    def Connect(self, request, context):
        # Store the client's connection details
        self.connections[request.client_id] = context
        print(f"Client {request.client_id} connected.")
        return private_chat_pb2.ConnectResponse(success=True, message=f'Connected with ID: {request.client_id}')

    def SendMessage(self, request, context):
        # Send the message to the target user identified by request.target_id
        target_connection = self.connections.get(request.target_id)
        if target_connection:
            try:
                target_connection.send_message(request)  # Send message to target client
                print(f"Message sent from {request.sender_id} to {request.target_id}: {request.content}")
            except Exception as e:
                print(f"Error sending message to client {request.target_id}: {e}")
        else:
            print(f"Target user {request.target_id} not found.")
        return private_chat_pb2.Empty()  # Empty response as acknowledgment

    def ReceiveMessage(self, request, context):
        # Implement logic to handle receiving messages
        pass  # No need to implement this for the server

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    private_chat_pb2_grpc.add_PrivateChatServicer_to_server(PrivateChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def register_user_info(username):
    # Generate a random UUID as the client ID
    client_id = str(uuid.uuid4())

    # Register user's data (IP, port, name, and ID) in the name server
    ip_address = socket.gethostbyname(socket.gethostname())
    port = 50051  # Set the default port

    name_server.register_user(chat_id=client_id,ip_address=ip_address,port=port,username=username)

    return {'ip': ip_address, 'port': port, 'id': client_id}


if __name__ == '__main__':
    serve()