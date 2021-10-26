from logging import Logger
from abc import abstractmethod
from jimmy.messages import Message
from jimmy.messages.responses import Response
# from jimmy.include.mixins.process_data import ProcessDictMixin
from .message_processor import MessageProcessor
from db import Session
from db.schema import Client, ClientHistory, ContactList


class ServerMessageProcessor(MessageProcessor):
    _message_processors = {
        'quit': ProcessQuit,
        'add_contact': ProcessAddContact,
        'del_contact': ProcessDelContact,
        'get_contacts': ProcessGetContacts,

    }

    def __init__(self, logger: Logger):
        super().__init__()
        self.session = Session()
        self.logger = logger

    def _get_processor(self, message: Message) -> 'Process':
        message_type = message.get_type()
        processor = self._message_processors.get(message_type)
        return processor()

    def process_message(self, message: Message) -> Response:
        processor = self._get_processor()
        processor.action(self.session, self.logger)
        response = processor.get_response()
        return response


class Process:
    def __init__(self, message: Message):
        self.message = message

    def _get_response_object(self, code, payload=None) -> Response:
        ResponseType = Response.response_types.get(code)
        if payload:
            response = ResponseType(payload)
        else:
            response = ResponseType()

        return response

    @abstractmethod
    def action(self, session: Session, logger: Logger) -> None:
        pass

    @abstractmethod
    def get_response(self) -> Response:
        pass


class ProcessQuit(Process):
    def action(self, session: Session, logger: Logger) -> None:
        logger.info(str(self.message))
        logger.warning(f'Get a "quit" message shutting down')

    def get_response(self) -> Response:
        return self._get_response_object(200)


class ProcessAddContact(Process):
    def action(self, session: Session, logger: Logger) -> None:
        logger.info(str(self.message))
        client = ContactList(owner_id=self.message.body.get('user_login'), user_id=self.message.body.get('user_id'))
        session.add(client)
        session.commit()

   def get_response(self) -> Response:
        return self._get_response_object(200)


class ProcessDelContact(Process):
    def action(self, session: Session, logger: Logger) -> None:
        logger.info(str(self.message))
        client = ContactList(owner_id=self.message.body.get('user_login'), user_id=self.message.body.get('user_id'))
        session.delete(client)
        session.commit()

   def get_response(self) -> Response:
        return self._get_response_object(200)


class ProcessGetContacts(Process):
    def action(self, session: Session, logger: Logger) -> None:
        logger.info(str(self.message))

        return contacts

   def get_response(self, session: Session) -> Response:
        contacts = session.query(ContactList).filter_by(user_id=message.body.get('user_id'))
        response = self._get_response_object(202, payload=contacts)
        return response

