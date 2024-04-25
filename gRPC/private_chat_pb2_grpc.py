# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import private_chat_pb2 as private__chat__pb2


class PrivateChatStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Connect = channel.unary_unary(
                '/PrivateChat/Connect',
                request_serializer=private__chat__pb2.ConnectRequest.SerializeToString,
                response_deserializer=private__chat__pb2.ConnectResponse.FromString,
                )
        self.Disconnect = channel.unary_unary(
                '/PrivateChat/Disconnect',
                request_serializer=private__chat__pb2.DisconnectRequest.SerializeToString,
                response_deserializer=private__chat__pb2.Empty.FromString,
                )
        self.SendMessage = channel.unary_unary(
                '/PrivateChat/SendMessage',
                request_serializer=private__chat__pb2.Message.SerializeToString,
                response_deserializer=private__chat__pb2.Empty.FromString,
                )
        self.ReceiveMessage = channel.unary_unary(
                '/PrivateChat/ReceiveMessage',
                request_serializer=private__chat__pb2.ReceiveMessageRequest.SerializeToString,
                response_deserializer=private__chat__pb2.ReceiveMessageResponse.FromString,
                )


class PrivateChatServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Connect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Disconnect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReceiveMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PrivateChatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Connect': grpc.unary_unary_rpc_method_handler(
                    servicer.Connect,
                    request_deserializer=private__chat__pb2.ConnectRequest.FromString,
                    response_serializer=private__chat__pb2.ConnectResponse.SerializeToString,
            ),
            'Disconnect': grpc.unary_unary_rpc_method_handler(
                    servicer.Disconnect,
                    request_deserializer=private__chat__pb2.DisconnectRequest.FromString,
                    response_serializer=private__chat__pb2.Empty.SerializeToString,
            ),
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=private__chat__pb2.Message.FromString,
                    response_serializer=private__chat__pb2.Empty.SerializeToString,
            ),
            'ReceiveMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveMessage,
                    request_deserializer=private__chat__pb2.ReceiveMessageRequest.FromString,
                    response_serializer=private__chat__pb2.ReceiveMessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PrivateChat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PrivateChat(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Connect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PrivateChat/Connect',
            private__chat__pb2.ConnectRequest.SerializeToString,
            private__chat__pb2.ConnectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Disconnect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PrivateChat/Disconnect',
            private__chat__pb2.DisconnectRequest.SerializeToString,
            private__chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PrivateChat/SendMessage',
            private__chat__pb2.Message.SerializeToString,
            private__chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReceiveMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PrivateChat/ReceiveMessage',
            private__chat__pb2.ReceiveMessageRequest.SerializeToString,
            private__chat__pb2.ReceiveMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
