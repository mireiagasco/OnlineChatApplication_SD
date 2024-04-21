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
    def __init__(self):
        self.messages = []

    def Connect(self, request, context):
        return private_chat_pb2.ConnectResponse(success=True, message=f'Connected with ID: {request.client_id}')

    def SendMessage(self, request, context):
        # Extract sender ID, destination ID, and message content from the request
        sender_id = request.sender_id
        destination_id = request.recipient_id
        message_content = request.content

        self.messages.append({"sender": sender_id, "destination": destination_id, "message": message_content})
        return private_chat_pb2.Empty()  # Return an empty response

    def ReceiveMessage(self, request, context):
        sender_id = request.sender_id
        recipient_id = request.recipient_id
        matching_message = None

        for message in self.messages:
            if message['sender'] == sender_id and message['destination'] == recipient_id:
                matching_message = message
                self.messages.remove(message)  # Remove the matching message from the queue
                break

        if matching_message:
            return private_chat_pb2.ReceiveMessageResponse(
                message=private_chat_pb2.Message(
                    sender_id=matching_message['sender'],
                    recipient_id=matching_message['destination'],
                    content=matching_message['message']
                )
            )
        else:
            return private_chat_pb2.ReceiveMessageResponse(
                empty=private_chat_pb2.Empty()  # Return an empty response if no matching message is found
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    private_chat_pb2_grpc.add_PrivateChatServicer_to_server(PrivateChatService(), server)
    server.add_insecure_port('[::]:50051')
    print("Listening on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()