import json
import logging
from socket import socket, error, AF_INET, SOCK_STREAM

from jimmy.messages.message import Message
from jimmy.messages.responses import Response
from jimmy.include.logger import LoggerMixin
from jimmy.include.decorators import log


class Client(LoggerMixin):
    _logname = 'client'

    def __init__(self, **kwargs):
        self.socket = socket(AF_INET, SOCK_STREAM)

        self.ANONYMOUS = 'anonymous'
        self.server_addr = kwargs.get('server_addr')
        self.server_port = kwargs.get('server_port')

        self.logdir = kwargs.get('logdir', './log')
        self.logfile = kwargs.get('logfile', 'client.log')
        self.loglevel = kwargs.get('loglevel', logging.INFO)
        self.logger = self._get_logger(self._logname, self.logdir, self.logfile, self.loglevel)

        self.account_name = kwargs.get('account_name', self.ANONYMOUS)

        self.message_type = kwargs.get('message_type')

    def start(self):
        try:
            self.socket.connect((self.server_addr, self.server_port))
        except error:
            self.logger.error(f'Cant establish connection to {self.server_addr}:{self.server_port}')
        else:
            # msg = self.socket.recv(1024)
            self._send_message(self.message_type, account_name=self.account_name)
            data = self.socket.recv(10240)
            self._process_response(data)

            self.socket.close()

    def _send_message(self, message_type, **body):
        if message_type in Message.message_types:
            ConcreteMessageType = Message.message_types.get(message_type)
            message = ConcreteMessageType(**body)
            data = message.get_data()
            self.socket.send(data)
            self.logger.info(f'Request: {str(message)}')
        else:
            self.logger.warning(f'Unknown message type: {message_type}')
            self.logger.warning(Message.message_types)

    @log
    def _process_response(self, data):
        response_dict = json.loads(data.decode('utf-8'))
        code = response_dict.get('response')
        ResponseType = Response.response_types.get(code)
        response = ResponseType()
        self.logger.info(f'Responce: {str(response)}')
