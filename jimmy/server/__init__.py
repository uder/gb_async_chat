import json
import logging
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime

from jimmy.messages.message import Message
from jimmy.messages.responses import Response
from jimmy.include.logger import LoggerMixin


class Server(LoggerMixin):
    _logname = 'server'

    def __init__(self, **kwargs):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self._running = True

        self.addr = kwargs.get('server_addr')
        self.port = int(kwargs.get('server_port'))
        self.max_client = kwargs.get('max_client', 5)
        
        self.logdir = kwargs.get('logdir', './log')
        self.logfile = kwargs.get('logfile', 'server.log')
        self.loglevel = kwargs.get('loglevel', logging.INFO)
        self.logger = self._get_logger(self._logname, self.logdir, self.logfile, self.loglevel)
        
    def start(self):
        self.socket.bind((self.addr, self.port))
        self.socket.listen(self.max_client)
        self._run()

    def _run(self):
        while self._running:
            client, addr = self.socket.accept()
            now = datetime.now().isoformat()
            # print('client accepted', now, str(addr))
            self.logger.info(f'client accepted {str(addr)}')
            data = client.recv(102400)
            if data:
                response = self._process_message(data)
                client.send(response.get_data())
            client.close()
        client.close()

    def _process_message(self, data: bytes) -> Response:
        message_dict = json.loads(data.decode('utf-8'))
        message_type = message_dict.get('action')
        ConcreteMessageType = Message.message_types.get(message_type)
        message = ConcreteMessageType(**message_dict)
        # print(message)
        self.logger.info(str(message))

        response = self._get_response(200)
        if message_type == 'quit':
            self._running = False

        return response

    def _get_response(self, code: int) -> Response:
        ResponseType = Response.response_types.get(code)
        response = ResponseType()
        return response
