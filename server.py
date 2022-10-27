from argparse import ArgumentParser
import socket

from lib import (
    make_directory,
    make_request_details,
    report,
    valid_file,
    packets_needed,
    make_qualifier,
    receive_file,
    send_file,
    send_list,
    list_files
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
    qualify = make_qualifier("server_files")
    if not valid_file(qualify, name):
        return (False, make_ack(1, "File not found", 0))
    packets = packets_needed(qualify, name)
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


def transfer(
    type: int,
    packets: int,
    sock_server: socket.socket,
    sock_client: socket.socket,
    name: str = "",
) -> None:
    """Do the data transfer after a successful handshake"""
    server_qualify = make_qualifier("server_files")
    client_qualify = make_qualifier("client_files")
    if type == 0:
        send_file(sock_client, packets_needed(
            server_qualify, name), server_qualify(name))
    elif type == 1:
        receive_file(sock_client, packets, server_qualify(name))
    else:
        send_list(sock_client, list_files(server_qualify))


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "port", type=int, help="The port that the server should listen on"
    )
    return vars(parser.parse_args())


def to_request(request_name: int) -> str:
    status_dict = {0: "get", 1: "put", 2: "list"}
    return status_dict[request_name]


def main():
    try:
        make_directory("server_files")
    except (FileExistsError):
        pass
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
                return

            success, ack = handle_request(request)
            client.sendall(ack.encode("utf-8"))
            if success:
                transfer(request["type"], request["n"],
                         sock, client, request["name"])
                request_details = make_request_details(
                    addr[0], addr[1], to_request(request["type"]), request["name"] if request["name"] != "" else "N/A", 0 if success else 1)
                print(report(request_details))


if __name__ == "__main__":
    main()
