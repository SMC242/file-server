from argparse import ArgumentParser
import socket

from lib import (
    valid_file,
    packets_needed,
    qualify,
    receive_file,
    send_file,
    send_list,
    list_files,
)
from request import to_fields, validate_initial, make_ack, validate_type

IP = "127.0.0.1"  # localhost
MAX_CONNECTIONS = 5

RetAddress = tuple[str, int]
# (success, message)
HandlerResponse = tuple[bool, str]


def map_values(keys: list[str], f, d: dict) -> dict:
    """Apply a function to the values of the given keys"""
    return d | {k: f(d[k]) for k in keys}


def read_initial_req(addr: RetAddress, response: bytes) -> dict | None:
    fields = to_fields(response.decode("utf-8"))
    if not validate_initial(fields) or not validate_type(fields["type"]):
        return None
    return map_values(["type", "n"], int, fields)  # Cast integer fields


def handle_get(name: str) -> HandlerResponse:
    if not valid_file(name):
        return (False, make_ack(1, "File not found", 0))
    packets = packets_needed(qualify(name))
    return (True, make_ack(0, "", packets))


def handle_put(name: str) -> HandlerResponse:
    return (True, make_ack(0, "", 0))


def handle_list() -> HandlerResponse:
    return (True, make_ack(0, "", 0))


def handle_request(fields: dict) -> tuple[bool, str]:
    """Form an acknowledgement based on the request. Also return a success/failure flag"""
    HANDLERS = {
        0: handle_get,
        1: handle_put,
        2: lambda x: handle_list(),  # Absorb the `name` field
    }

    f = HANDLERS.get(fields["type"])
    if not f:
        return (False, make_ack(1, "Invalid request type", 0))
    return f(fields["name"])


def transfer(type: int, packets: int, sock: socket.socket, name: str = "") -> None:
    """Do the data transfer after a successful handshake"""
    if type == 0:
        send_file(sock, packets, qualify(name))
    elif type == 1:
        receive_file(sock, packets, qualify(name))
    else:
        send_list(sock, list_files())


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
            if not request:
                client.sendall(
                    make_ack(1, "Malformed request", 0).encode("bytes"))

            success, ack = handle_request(request)
            client.sendall(ack)
            if success:
                receive(fields["type"], fields["n"])


if __name__ == "__main__":
    main()
