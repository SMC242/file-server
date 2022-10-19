from argparse import ArgumentParser
import socket

from lib import format_address, RequestDetails, make_request_details
from request import to_fields, validate_initial

IP = "127.0.0.1"  # localhost
MAX_CONNECTIONS = 5

RetAddress = tuple[str, int]


def read_initial_req(addr: RetAddress, response: bytes) -> dict | None:
    fields = to_fields(response.decode("utf-8"))
    return fields if validate_initial(fields) else None


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "port", type=int, help="The port that the server should listen on"
    )
    return vars(parser.parse_args())


def main():
    args = parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((IP, args["port"]))
        sock.listen(MAX_CONNECTIONS)
        print("Server started")

        client, addr = sock.accept()
        with client:  # Automatically close the connection
            request = read_initial_req(addr, client.recv(1024))


if __name__ == "__main__":
    main()
