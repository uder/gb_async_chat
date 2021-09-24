from typing import Union

from jimmy.messages import Message, MessageFactory
from jimmy.messages.responses import Response, ResponseFactory


class ProcessDictMixin:
    def _process_data(self, data_dict: dict) -> Union[Message, Response]:

        if data_dict.get('response'):
            result = ResponseFactory.create_response(data_dict)
        elif data_dict.get('action'):
            result = MessageFactory.create_message(data_dict)
        else:
            self.logger.warning(f'Malformed data: {data_dict}')
            result = ResponseFactory.create_by_code(299)
        return result
