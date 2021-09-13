import argparse
from jimmy.server import Server


def _parse_args():
    descr = "Jimmy server"
    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument("-a", "--addr", help="Server's address", dest='server_addr', default='localhost', type=str)
    parser.add_argument("-p", "--port", help="Server's port", dest='server_port', default=7777, type=int)
    parser.add_argument("-l", "--logdir", help="Server's logging dir", dest='logdir', default='./log', type=str)
    args = vars(parser.parse_args())

    return args


def main():
    kwargs = _parse_args()
    server = Server(**kwargs)
    server.start()


if __name__ == '__main__':
    main()
