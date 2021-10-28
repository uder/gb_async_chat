from .client import Client


class SenderClient(Client):
    _logname = 'sender_client'

    def start(self):
        try:
            self.socket.connect((self.server_addr, self.server_port))
        except Exception as err:
            self.logger.error(
                f'Cant establish connection to {self.server_addr}:{self.server_port}')
        else:
            self._send_message(
                self.message_type,
                account_name=self.account_name)

            self.socket.close()
