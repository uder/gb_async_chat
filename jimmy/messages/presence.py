import json
from datetime import datetime

from .message import Message


class PresenceMessage(Message):
    _type = 'presence'

    def _parse_body(self):
        result_dict = {}
        result_dict.update({'action': self._type})
        result_dict.update({'time': str(datetime.now().timestamp())})

        if self.body.get('type'):
            result_dict.update({'type': self.body.get('type')})

        user_dict = {}
        user_dict.update({'account_name': self.body.get('account_name')})
        user_dict.update({'status': 'Yep, I am here!'})
        result_dict.update({'user': user_dict})

        return json.dumps(result_dict)
