import json
from datetime import datetime

from .message import Message


class QuitMessage(Message):
    _type = 'quit'

    def _parse_body(self):
        result_dict = {}
        result_dict.update({'action': self._type})
        result_dict.update({'time': str(datetime.now().timestamp())})

        return json.dumps(result_dict)
