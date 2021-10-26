import json
from abc import abstractmethod

from jimmy.include.message_mapper import MessageMapper


class ResponseFactory:
    @staticmethod
    def create_response(response_dict: dict) -> 'Response':
        if response_dict.get('response') in Response.response_types:
            response_type = Response.response_types.get(response_dict.get('response'))
        else:
            response_type = Response.response_types.get(299)

        response = response_type()

        return response
    @staticmethod
    def create_by_code(code: int) -> 'Response':
        if code in Response.response_types:
            response_type = Response.response_types.get(code)
        else:
            response_type = Response.response_types.get(299)

        response = response_type()
        return response

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


class Response202(Response):
    _code = 202
    _alert = "Список контактов"

    def __init__(self, contact_list: list):
        self.contact_list = contact_list
        super().__init__()

    def _get_json(self):
        result_dict = {}
        result_dict.update({'response': self._code})
        result_dict.update({'alert': self.contact_list})

        return json.dumps(result_dict)


class Response299(Response):
    _code = 299
    _alert = "Пустое сообщение. Только для тестов"

    def _get_json(self):
        result_dict = {}
        result_dict.update({'response': self._code})
        result_dict.update({'alert': self._alert})

        return json.dumps(result_dict)

