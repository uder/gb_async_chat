from .server import Server
from select import select

class TestServer(Server):
    def start(self):
        print(f'Listening on {self.addr}:{self.port}')
        self.socket.bind((self.addr, self.port))
        self.socket.listen(self.max_client)
        self.socket.settimeout(3)
        # self.socket.setblocking(False)
        self._run()

    def _run(self):
        # counter = 0
        data = '{"test_server": "true"}'.encode('utf-8')
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
                print(client, addr)
                try:
                    print('send data')
                    client.send(data)
                except:
                    pass
                # client.close()
            #     self.logger.info(f'client accepted {str(addr)}')
            #     client_list.append(client)
            # finally:
            #     try:
            #         rlist, wlist, elist = select(client_list, client_list, elist, wait)
            #         print(rlist, wlist)
            #     except OSError as err:
            #         # print(err)
            #         pass
            #     else:
            #         for wclient in wlist:
            #             wclient.send(data)