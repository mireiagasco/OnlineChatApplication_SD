from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class ConnectResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class DisconnectRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("sender_id", "recipient_id", "content")
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    sender_id: str
    recipient_id: str
    content: str
    def __init__(self, sender_id: _Optional[str] = ..., recipient_id: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class ReceiveMessageRequest(_message.Message):
    __slots__ = ("sender_id", "recipient_id")
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    sender_id: str
    recipient_id: str
    def __init__(self, sender_id: _Optional[str] = ..., recipient_id: _Optional[str] = ...) -> None: ...

class ReceiveMessageResponse(_message.Message):
    __slots__ = ("message", "empty", "disconnect_message")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EMPTY_FIELD_NUMBER: _ClassVar[int]
    DISCONNECT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: Message
    empty: Empty
    disconnect_message: DisconnectMessage
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ..., empty: _Optional[_Union[Empty, _Mapping]] = ..., disconnect_message: _Optional[_Union[DisconnectMessage, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DisconnectMessage(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
