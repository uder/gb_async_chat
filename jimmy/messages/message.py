from abc import abstractmethod

from jimmy.include.message_mapper import MessageMapper

class MessageFactory:
    @staticmethod
    def create_message(message_dict: dict) -> 'Message':
        if message_dict.get('action') in Message.message_types:
            message_type = Message.message_types.get(message_dict.get('action'))
        else:
            message_type = Message.message_types.get('not_existent_action')

        message = message_type(**message_dict)

        return message


class Message(metaclass=MessageMapper):
    message_types = {}
    _type = 'unknown'

    @classmethod
    def _register(cls):
        cls.message_types.update({cls._type: cls})

    def __init__(self, **body):
        self.body = body
        self.json = self._parse_body()
        self.json_encoded = self.json.encode('utf-8')

    def __str__(self):
        return self.json

    @abstractmethod
    def _parse_body(self):
        pass

    def get_data(self):
        return self.json_encoded
