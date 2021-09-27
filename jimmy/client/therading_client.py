from threading import Thread

from .client import Client


class ThreadingClient(Client):
    _logname = 'threading_client'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.encoding = 'utf-8'
        self._sender_running = True
        self._receiver_running = True

        self.send_to = '_BROADCAST'

    def start(self):
        thread_sender = Thread(target=self._sender)
        thread_receiver = Thread(target=self._receiver)


    def _receiver(self):
        while self._receiver_running:
            response = None
            try:
                self.socket = socket(AF_INET, SOCK_STREAM)
                self.socket.connect((self.server_addr, self.server_port))
            except Exception as err:
                pass
            else:
                try:
                    data = socket.recv(10240)
                    if data:
                        response = self._process_response(data)
                        message_body = self._get_message_body(data)
                        message_from = self._get_from(data)

                    if message_from and message_body:
                        print(f'{message_from}: {message_body}')

                except Exception as err:
                    response = None
                self.socket.close()

            # if response:
            #     print(f'{datetime.now()} Response = {response}')
            #     self.logger.info(f'Response = {response}')


    def _sender(self):
        while self._sender_running:
            message_body = input("Send> ")

            if message_body == '_quit':
                self._kill()

            try:
                self.socket.connect((self.server_addr, self.server_port))
            except Exception as err:
                self.logger.error(f'Cant establish connection to {self.server_addr}:{self.server_port}')
            else:
                self._send_message('msg', from=self.account_name, to=self.send_to, encoding=self.encoding, message=message_body)
                self.socket.close()

    def _kill(self):
        self._sender_running = False
        self._receiver_running = False