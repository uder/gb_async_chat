import pytest
from jimmy.messages import Message
from jimmy.messages.responses import Response, Response200
from jimmy.server import Server


@pytest.fixture()
def args():
    args_server = {
        'server_addr': 'localhost',
        'server_port': 7777,
    }
    return args_server


@pytest.fixture()
def data():
    msg_dict = {
        "type": "presence",
        "account_name": "test_user",
    }
    message_class = Message.message_types.get(msg_dict.get('type'))
    message = message_class(**msg_dict)
    data = message.get_data()
    return data


@pytest.fixture()
def server(args):
    return Server(**args)


def test_get_responce(server):
    responce = server._get_response(200)
    assert isinstance(responce, Response200)


def test_process_message(server, data):
    responce = server._process_message(data)
    assert isinstance(responce, Response)
