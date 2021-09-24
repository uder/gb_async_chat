import json
from datetime import datetime

from .message import Message


class MsgMessage(Message):
    _type = 'msg'

    def _parse_body(self):
        result_dict = {}
        result_dict.update({'action': self._type})
        result_dict.update({'time': str(datetime.now().timestamp())})
        result_dict.update({'to': self.body.get('message_to')})
        result_dict.update({'from': self.body.get('message_from')})
        result_dict.update({'encoding': self.body.get('encoding')})
        result_dict.update({'message': self.body.get('message')})

        if self.body.get('type'):
            result_dict.update({'type': self.body.get('type')})

        return json.dumps(result_dict)
