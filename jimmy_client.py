import argparse
from jimmy.client import Client


def _parse_args():
    descr = "Client for a Jimmy server"
    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument("-a", "--addr", help="Server's address", dest='server_addr', default='localhost', type=str)
    parser.add_argument("-p", "--port", help="Server's port", dest='server_port', default=7777, type=int)
    parser.add_argument("-u", "--username", help="Your username", dest='account_name', default='test_user', type=str)

    parser.add_argument("-t", "--type", help="TEST Messge action", dest='message_type', default='presence', type=str)

    args = vars(parser.parse_args())

    return args


def main():
    args = _parse_args()
    client = Client(**args)
    client.start()


if __name__ == '__main__':
    main()
