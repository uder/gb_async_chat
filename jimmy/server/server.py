import json
import logging
from socket import socket, error, AF_INET, SOCK_STREAM
from select import select
from datetime import datetime

from jimmy.messages.message import Message
from jimmy.messages.responses import Response, ResponseFactory
from jimmy.include.logger import LoggerMixin
from jimmy.include.mixins.process_data import ProcessDictMixin
from jimmy.include.decorators import log
from jimmy.include.descriptors.socket import SocketDescriptorServer
# from db import Session
from jimmy.message_processor.server_processor import ServerMessageProcessor

class Server(LoggerMixin, ProcessDictMixin):
    _logname = 'server'
    socket = SocketDescriptorServer('socket')

    def __init__(self, **kwargs):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self._running = True
        # self.session = Session()

        self.addr = kwargs.get('server_addr')
        self.port = int(kwargs.get('server_port'))
        self.max_client = kwargs.get('max_client', 5)

        self.logdir = kwargs.get('logdir', './log')
        self.logfile = kwargs.get('logfile', 'server.log')
        self.loglevel = kwargs.get('loglevel', logging.INFO)
        self.logger = self._get_logger(self._logname, self.logdir, self.logfile, self.loglevel)
        self.message_processor = ServerMessageProcessor(self.logger)

    def start(self):
        self.logger.info(f'Listening on {self.addr}:{self.port}')
        self.socket.bind((self.addr, self.port))
        self.socket.listen(self.max_client)
        self.socket.settimeout(3)
        # self.socket.setblocking(False)
        self._run()

    def _run(self):
        response = None
        buffered_message = ResponseFactory.create_by_code(299)
        # counter = 0
        while self._running:
            # counter += 1
            # print(counter)
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
                    # print(rlist, wlist)
                except OSError as err:
                    # print(err)
                    pass
                else:
                    for rclient in rlist:
                        try:
                            rclient.setblocking(True)
                            data = rclient.recv(102400)
                            # print(data)
                        except:
                            self.logger.error(f'Cant read from {rclient}')
                        else:
                            if data:
                                print(data.decode('utf-8'))
                                response = self._process_message(data)
                                data_dict = json.loads(data.decode('utf-8'))
                                buffered_message = self._process_data(data_dict)
                            rclient.close()
                    for wclient in wlist:
                        try:
                            if buffered_message:
                                wclient.setblocking(True)
                                wclient.send(buffered_message.get_data())
                                buffered_message = None
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
        # self.logger.info(str(message))


        # response = self._get_response(200)
        response = self.message_processor.process_message(message)
        if message_type == 'quit':
            self._running = False
            # self.logger.warning(f'Get a "quit" message shutting down')

        # if message_type == 'add_contact':

        return response

    def _get_response(self, code: int) -> Response:
        ResponseType = Response.response_types.get(code)
        response = ResponseType()
        return response
