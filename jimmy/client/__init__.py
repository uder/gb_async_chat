import json

from socket import socket, AF_INET, SOCK_STREAM
from jimmy.messages.message import Message
from jimmy.messages.responses import Response


class Client:
    def __init__(self, **kwargs):
        self.socket = socket(AF_INET, SOCK_STREAM)

        self.ANONYMOUS = 'anonymous'
        self.server_addr = kwargs.get('server_addr')
        self.server_port = kwargs.get('server_port')

        self.account_name = kwargs.get('account_name', self.ANONYMOUS)

        self.message_type = kwargs.get('message_type')

    def start(self):
        self.socket.connect((self.server_addr, self.server_port))
        # msg = self.socket.recv(1024)
        # print(f"Message: {msg.decode('utf-8')}")
        self._send_message(self.message_type, account_name=self.account_name)
        data = self.socket.recv(10240)
        # print(data)
        self._process_response(data)

        self.socket.close()

    def _send_message(self, message_type, **body):
        if message_type in Message.message_types:
            ConcreteMessageType = Message.message_types.get(message_type)
            message = ConcreteMessageType(**body)
            data = message.get_data()
            self.socket.send(data)
            print(message)
        else:
            print(f'Unknown message type: {message_type}')
            print(Message.message_types)

    def _process_response(self, data):
        response_dict = json.loads(data.decode('utf-8'))
        code = response_dict.get('response')
        ResponseType = Response.response_types.get(code)
        response = ResponseType()
        print(response)
