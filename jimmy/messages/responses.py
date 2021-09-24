import json
from abc import abstractmethod

from jimmy.include.message_mapper import MessageMapper


class Response(metaclass=MessageMapper):
    response_types = {}
    _code = 0

    @classmethod
    def _register(cls):
        cls.response_types.update({cls._code: cls})

    def __init__(self):
        self.json = self._get_json()

    def __str__(self):
        return f'{self._code}'

    @abstractmethod
    def _get_json(self):
        pass

    def get_data(self):
        data = self.json.encode('utf-8')
        return data


class Response200(Response):
    _code = 200
    _alert = "Необязательное сообщение/уведомление"

    def _get_json(self):
        result_dict = {}
        result_dict.update({'response': self._code})
        result_dict.update({'alert': self._alert})

        return json.dumps(result_dict)

class Response299(Response):
    _code = 299
    _alert = "Пустое сообщение. Только для тестов"

    def _get_json(self):
        result_dict = {}
        result_dict.update({'response': self._code})
        result_dict.update({'alert': self._alert})

        return json.dumps(result_dict)
