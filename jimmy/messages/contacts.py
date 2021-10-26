import json
from datetime import datetime

from .message import Message


class AddContactMessage(Message):
    _type = 'add_contact'

    def _parse_body(self):
        result_dict = {}
        result_dict.update({'action': self._type})
        result_dict.update({'time': str(datetime.now().timestamp())})
        result_dict.update({'user_login': self.body.get('user_login')})
        result_dict.update({'user_id': self.body.get('user_id')})

        return json.dumps(result_dict)


class DelContactMessage(Message):
    _type = 'del_contact'

    def _parse_body(self):
        result_dict = {}
        result_dict.update({'action': self._type})
        result_dict.update({'time': str(datetime.now().timestamp())})
        result_dict.update({'user_login': self.body.get('user_login')})
        result_dict.update({'user_id': self.body.get('user_id')})

        return json.dumps(result_dict)


class GetContactsMessage(Message):
    _type = 'get_contacts'

    def _parse_body(self):
        result_dict = {}
        result_dict.update({'action': self._type})
        result_dict.update({'time': str(datetime.now().timestamp())})
        result_dict.update({'user_login': self.body.get('user_login')})

        return json.dumps(result_dict)
