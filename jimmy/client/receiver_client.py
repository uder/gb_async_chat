from datetime import datetime
from socket import socket, error, AF_INET, SOCK_STREAM

from .client import Client


class ReceiverClient(Client):
    _logname = 'receiver_client'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._running = True

    def start(self):
        def _get_response(socket):
            response = None
            data = socket.recv(10240)
            if data:
                response = self._process_response(data)
            return response

        while self._running:
            response = None
            try:
                self.socket = socket(AF_INET, SOCK_STREAM)
                self.socket.connect((self.server_addr, self.server_port))
            except Exception as err:
                pass
            else:
                try:
                    response = _get_response(self.socket)
                except Exception as err:
                    pass
                self.socket.close()

            if response:
                print(f'{datetime.now()} Response = {response}')
                self.logger.info(f'Response = {response}')

