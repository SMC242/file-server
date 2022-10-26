from argparse import ArgumentParser
import socket

from request import make_inital_req, to_fields, validate_ack
from lib import packets_needed, valid_file

# 1 KiB
PACKET_SIZE = 1024


def parse_ack(response: bytes) -> dict | None:
    """Validate and convert acknowledgement message into its fields"""
    fields = to_fields(response.decode("utf-8"))
    return fields if validate_ack(fields) else None


def make_requester(ip: str, port: int):
    """Get a function that will transmit a request of the given type"""

    def request_of(type: str):
        # The value will either be a file path or True (if --list)
        def with_arg(arg):
            if type == "get":
                code, name, n = 0, arg, 0
            elif type == "put":
                if not valid_file(arg):
                    raise ValueError("Invalid file name")
                code, name, n = 1, arg, packets_needed(arg)
            else:
                code, name, n = 2, "", 0
            req = make_inital_req(code, name, n)

            # Any exceptions raised will close the connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))

                sock.send(req)  # Initial request
                # Receive acknowledgement
                ack_fields = parse_ack(sock.recv(PACKET_SIZE))
                if not ack_fields:
                    raise ValueError(
                        "Received invalid response from server. Closing connection..."
                    )
                # Report any errors from the server
                elif ack_fields["status"] == "1":
                    raise Exception(ack_fields["msg"])

                # TODO: receive/send data

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
        if args[k] is None:
            print("Executing command")
            try:
                return commands[k](args[k])
            except Exception as e:
                return print(e.message)

    # No request made
    print(
        "Error: You must make a request with --get, --put, or --list. See --help for more info"
    )


if __name__ == "__main__":
    main()
