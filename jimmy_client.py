import argparse
from jimmy.client import Client, SenderClient, ReceiverClient


def _parse_args():
    descr = "Client for a Jimmy server"
    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument("-a", "--addr", help="Server's address", dest='server_addr', default='localhost', type=str)
    parser.add_argument("-p", "--port", help="Server's port", dest='server_port', default=7777, type=int)
    parser.add_argument("-u", "--username", help="Your username", dest='account_name', default='test_user', type=str)
    parser.add_argument("-l", "--logdir", help="Client's logging dir", dest='logdir', default='./log', type=str)

    parser.add_argument("-r", "--receive", help="TEST Read client", dest='receive', action='store_true', default=False)
    parser.add_argument("-s", "--send", help="TEST Write client", dest='send', action='store_true', default=False)

    parser.add_argument("-t", "--type", help="TEST Message action", dest='message_type', default='presence', type=str)

    args = vars(parser.parse_args())

    return args


def main():
    args = _parse_args()
    if args.get('send'):
        client = SenderClient(**args)
    elif args.get('receive'):
        client = ReceiverClient(**args)
    else:
        raise Exception("Client type (send/receive) id not defined")
    # client = Client(**args)
    client.start()


if __name__ == '__main__':
    main()
