import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from .client import Client
from jimmy.include.mixins.process_data import ProcessDictMixin


class ThreadingClient(Client, ProcessDictMixin):
    """Threading client implementation"""
    _logname = 'threading_client'

    def __init__(self, **kwargs):
        """Initialize Client instance"""
        super().__init__(**kwargs)
        self.encoding = 'utf-8'
        self._sender_running = True
        self._receiver_running = True

        self.send_to = '_BROADCAST'

    def start(self):
        """Entry point. Start your client with start()"""
        thread_sender = Thread(target=self._sender)
        thread_sender.start()
        thread_receiver = Thread(target=self._receiver)
        thread_receiver.start()

    def _get_socket(self):
        s = socket(AF_INET, SOCK_STREAM)
        return s

    def _receiver(self):
        """Receiver thread implementation"""
        while self._receiver_running:
            s = self._get_socket()

            try:
                s.connect((self.server_addr, self.server_port))
            except Exception as err:
                # print(f'Cant connect: {err}')
                pass

            try:
                data = s.recv(10240)
            except Exception as err:
                # print(f'Cant recv data: {err}')
                pass
            else:
                if data:
                    # print(data.decode('utf-8'))
                    data_dict = json.loads(data.decode('utf-8'))
                    message = self._process_data(data_dict)
                    print(f'\n{message}')
            s.close()

    def _sender(self):
        """Sender thread implementation"""
        while self._sender_running:
            s = self._get_socket()
            message_body = input("Send> ")

            if message_body == '_quit':
                self._kill()

            try:
                s.connect((self.server_addr, self.server_port))
            except Exception as err:
                # print(f'Cant connect: {err}')
                pass
            finally:
                message_dict = {
                    'action': 'msg',
                    'message_from': self.account_name,
                    'message_to': self.send_to,
                    'encoding': self.encoding,
                    'message': message_body,
                }
                message = self._process_data(message_dict)
                s.send(message.get_data())
                s.close()

    def _kill(self):
        """Stops client"""
        self._sender_running = False
        self._receiver_running = False

    def __del__(self):
        self.socket.close()
