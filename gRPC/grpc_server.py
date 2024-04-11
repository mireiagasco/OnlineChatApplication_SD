import grpc
from concurrent import futures
import os
import sys
import private_chat_pb2
import private_chat_pb2_grpc
from Redis.NameServer import NameServer

# Get the absolute path to the directory containing the module
module_dir = os.path.abspath("gRPC")
# Add the directory to the Python path
sys.path.append(module_dir)

name_server = NameServer()


class PrivateChatService(private_chat_pb2_grpc.PrivateChatServicer):

    def Connect(self, request, context):
        return private_chat_pb2.ConnectResponse(success=True, message=f'Connected with ID: {request.client_id}')

    def SendMessage(self, request, context):
        # Extract sender ID, destination ID, and message content from the request
        sender_id = request.sender_id
        destination_id = request.recipient_id
        message_content = request.content

        # Retrieve connection parameters associated with the destination ID from the NameServer
        connection_params = name_server.get_connection_params(destination_id)
        if not connection_params:
            # If destination ID is not found in the NameServer, return an error response
            return private_chat_pb2.Empty()

        # Extract IP address and port from the connection parameters
        destination_ip = connection_params[b'ip_address'].decode()
        destination_port = int(connection_params[b'port'])
        # Send the message to the destination client using the obtained connection parameters
        try:
            # Create a gRPC channel to the destination client
            channel = grpc.insecure_channel(f"{destination_ip}:{destination_port}")
            stub = private_chat_pb2_grpc.PrivateChatStub(channel)

            # Create and send the message
            message = private_chat_pb2.Message(sender_id=sender_id, recipient_id=destination_id, content=message_content)
            stub.ReceiveMessage(message)

            # Return an empty response as acknowledgment
            return private_chat_pb2.Empty()

        except Exception as e:
            # Handle any errors that occur during message transmission
            print(f"Error sending message to client {destination_id}: {e}")
            return private_chat_pb2.Empty()

    def ReceiveMessage(self, request_iterator, context):
        return private_chat_pb2.Empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    private_chat_pb2_grpc.add_PrivateChatServicer_to_server(PrivateChatService(), server)
    server.add_insecure_port('[::]:50051')
    print("Listening on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()