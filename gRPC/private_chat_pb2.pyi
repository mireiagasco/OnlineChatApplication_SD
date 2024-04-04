from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectRequest(_message.Message):
    __slots__ = ("client_id", "ip_address", "port", "username")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    ip_address: str
    port: int
    username: str
    def __init__(self, client_id: _Optional[str] = ..., ip_address: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ...) -> None: ...

class ConnectResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("sender", "content")
    SENDER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    content: str
    def __init__(self, sender: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
