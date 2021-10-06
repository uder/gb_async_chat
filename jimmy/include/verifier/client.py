from socket import socket
from . import VerifyMeta


class ClientVerifyMeta(VerifyMeta):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, socket):
                raise ValueError('ERROR: Class level socket definition is forbidden')