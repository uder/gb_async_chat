import pytest
import json
import os
import subprocess

from copy import deepcopy
from jimmy.client import Client


@pytest.fixture()
def args_client():
    args_client = {
        'server_addr': 'localhost',
        'server_port': 7777,
        'username': 'test_user',
    }
    return args_client


@pytest.fixture(scope="session", autouse=True)
def start_server(request):
    args_server = {
        'addr': 'localhost',
        'port': 7777,
    }

    executeable = os.path.join('venv', 'Scripts', 'python.exe')
    server_script = os.path.join('jimmy_server.py')
    args_list = [executeable, server_script]
    # for key, value in args_server.items():
    #     item = [f"--{key}", value]
    #     args_list.extend(item)

    def stop_server():
        try:
            server.wait(timeout=3)
        except Exception as err:
            pass

    print(args_list)
    server = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    request.addfinalizer(stop_server)


def test_client_send_presense_message(capsys, args_client):
    local_args = deepcopy(args_client)
    pointer = 0
    actions = ['presence', 'quit']

    for action in actions:
        local_args.update({'message_type': action})
        pointer += 1
        client = Client(**local_args)
        client.start()

    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    for index, line in enumerate(lines):
        line_dict = {}
        if index % 2 == 0:
            """ json line"""
            try:
                line_dict = json.loads(line)
            except Exception as err:
                pass

            message_type = line_dict.get('action')
            for j, action in enumerate(actions):
                if action == message_type:
                    assert (index, message_type) == (j*2, action)
        else:
            """ responce code line"""
            assert line == '200'

    with capsys.disabled():
        print(captured.out)
