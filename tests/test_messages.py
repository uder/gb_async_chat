import pytest
from jimmy.messages import Message
from jimmy.messages import PresenceMessage
from jimmy.messages import QuitMessage
from jimmy.messages.responses import *


def test_message_presence():
    message_class = Message.message_types.get('presence')
    message = message_class()

    assert isinstance(message, PresenceMessage)


def test_message_quit():
    message_class = Message.message_types.get('quit')
    message = message_class()

    assert isinstance(message, QuitMessage)


def test_response_200():
    responce_class = Response.response_types.get(200)
    response = responce_class()

    assert isinstance(response, Response200)
