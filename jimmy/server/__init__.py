import json
import logging
from socket import socket, error, AF_INET, SOCK_STREAM
from select import select
from datetime import datetime

from jimmy.messages.message import Message
from jimmy.messages.responses import Response
from jimmy.include.logger import LoggerMixin
from jimmy.include.decorators import log


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
        self.logger.info(f'Listening on {self.addr}:{self.port}')
        self.socket.bind((self.addr, self.port))
        self.socket.listen(self.max_client)
        self.socket.settimeout(3)
        # self.socket.setblocking(False)
        self._run()

    def _run(self):
        response = None
        while self._running:
            wait = 3
            client_list = []
            elist = []

            try:
                client, addr = self.socket.accept()
            except KeyboardInterrupt:
                self.logger.error('Ctrl+C is pressed. Server is stopped')
                self.socket.close()
                break
            except Exception as err:
                continue
            else:
                self.logger.info(f'client accepted {str(addr)}')
                client_list.append(client)
            finally:
                try:
                    rlist, wlist, elist = select(client_list, client_list, elist, wait)
                except OSError as err:
                    print(err)
                    pass
                else:
                    for rclient in rlist:
                        try:
                            rclient.setblocking(True)
                            data = rclient.recv(102400)
                        except:
                            self.logger.error(f'Cant read from {rclient}')
                        else:
                            if data:
                                response = self._process_message(data)
                            rclient.close()
                    for wclient in wlist:
                        try:
                            if response:
                                wclient.setblocking(True)
                                wclient.send(response.get_data())
                                response = None
                            wclient.close()
                        except:
                            self.logger.error(f'Cant write to {wclient}')
                finally:
                    pass

    @log
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
            self.logger.warning(f'Get a "quit" message shutting down')

        return response

    def _get_response(self, code: int) -> Response:
        ResponseType = Response.response_types.get(code)
        response = ResponseType()
        return response
