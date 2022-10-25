from argparse import ArgumentParser
import socket

from request import make_inital_req


def get(name: str) -> str:
    """Create a get message"""
    return make_inital_req(0, name, 0)


def put(name: str) -> str:
    """Create a put message"""
    return make_inital_req(type, name, n)


def put():
    pass


def make_requester(ip: str, port: int):
    """Get a function that will transmit a request of the given type"""
    CONVERSIONS = {"get": 0, "put": 1, "list": 2}

    def request_of(type: str):
        def with_name(file_name: str = ""):
            type_no = CONVERSIONS[type]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                req = make_inital_req(type_no, file_name, n)

    return request_of


def get_args() -> dict:
    parser = ArgumentParser()
    parser.add_argument("ip", type=str, help="IP of server")
    parser.add_argument("port", type=int, help="Port number of server")
    # Request types
    parser.add_argument(
        "-g",
        "--get",
        type=str,
        help="Download a file from the server. File name required",
    )
    parser.add_argument(
        "-p",
        "--put",
        type=str,
        help="Upload a file to the server. File name required",
    )
    parser.add_argument(
        "-l",
        "--list",
        help="List the available files on the server",
        action="store_true",  # The "list" key will be set to True if used
    )
    return vars(parser.parse_args())


def main():
    REQUEST_TYPES = ("get", "put", "list")

    args = get_args()
    request_of = make_requester(ip, port)
    commands = {t: lambda: request_of(t) for t in REQUEST_TYPES}

    for k in commands:
        # NOTE: empty file paths will fall through this (on purpose)
        if args[k]:
            print("executing")
            return commands[k]()

    # No request made
    print(
        "Error: You must make a request with --get, --put, or --list. See --help for more info"
    )


if __name__ == "__main__":
    main()
