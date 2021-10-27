import json
from datetime import datetime

from .message import Message


class AuthenticateMessage(Message):
    _type = 'authenticate'

    def _parse_body(self):
        result_dict = {}
        result_dict.update({'action': self._type})
        result_dict.update({'time': str(datetime.now().timestamp())})

        user_dict = {}
        user_dict.update({'account_name': self.body.get('account_name')})
        user_dict.update({'password': self.body.get('password')})
        result_dict.update({'user': user_dict})

        return json.dumps(result_dict)
