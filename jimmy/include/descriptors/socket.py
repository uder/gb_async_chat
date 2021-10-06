from abc import abstractmethod
from socket import socket, AF_INET, SOCK_STREAM


class SocketDescriptor:
    def __init__(self, name):
        self.name = '_' + name
        self.default = None

    def __set__(self, instance, s: socket):
        self.validate_socket(s)
        setattr(instance, self.name, s)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __delete__(self, instance):
        raise NotImplemented('ERROR: Socket deletion is not implemented')

    @abstractmethod
    def validate_socket(self, s: socket) -> None:
        pass


class SocketDescriptorClient(SocketDescriptor):
    def validate_socket(self, s: socket) -> None:
        if not (s.family == AF_INET and s.type == SOCK_STREAM):
            raise ValueError("ERROR: wrong socket config")


class SocketDescriptorServer(SocketDescriptor):
    def validate_socket(self, s: socket) -> None:
        pass
