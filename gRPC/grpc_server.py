import grpc
from concurrent import futures
import private_chat_pb2
import private_chat_pb2_grpc
import uuid
from Redis.NameServer import NameServer

name_server = NameServer()


class PrivateChatService(private_chat_pb2_grpc.PrivateChatServicer):
    def Connect(self, request, context):
        # Generate a random UUID as the client ID
        client_id = str(uuid.uuid4())

        # Register the chat with the name server
        name_server.register_client(client_id, request.ip_address, request.port, request.user_id)

        # Respond to the client with the assigned ID
        return private_chat_pb2.ConnectResponse(
            success=True,
            message=f'Connected with ID: {client_id}'
        )

    def SendMessage(self, request, context):
        # Implement logic to handle incoming messages
        # Broadcast the message to the appropriate client
        return private_chat_pb2.Empty() # Empty response as acknowledgment

    def ReceiveMessage(self, request, context):
        # Implement logic to handle receiving messages
        # Receive message from the client
        # Return the received message
        return private_chat_pb2.Message(sender="sender", content="Hello")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    private_chat_pb2_grpc.add_PrivateChatServicer_to_server(PrivateChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()