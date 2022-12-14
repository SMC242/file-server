from argparse import ArgumentParser
import socket

from request import make_inital_req, to_fields, validate_ack
from lib import make_directory, packets_needed, receive_file, receive_list, send_file, valid_file, PACKET_SIZE, make_qualifier, make_request_details, report


def parse_ack(response: bytes) -> dict | None:
    """Validate and convert acknowledgement message into its fields"""
    fields = to_fields(response.decode("utf-8"))
    return fields if validate_ack(fields) else None


def make_requester(ip: str, port: int):
    """Get a function that will transmit a request of the given type"""

    def request_of(type: str):
        # The value will either be a file path or True (if --list)
        def with_arg(arg):
            client_qualify = make_qualifier("client_files")
            server_qualify = make_qualifier("server_files")

            if type == "get":
                code, name, n = 0, arg, 0
            elif type == "put":
                if not valid_file(client_qualify, arg):
                    raise ValueError("Invalid file name")
                code, name, n = 1, arg, packets_needed(client_qualify, arg)
            else:
                code, name, n = 2, "", 0
            req = make_inital_req(code, name, n)

            # Any exceptions raised will close the connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))

                sock.send(req.encode("utf-8"))  # Initial request
                # Receive acknowledgement
                ack_fields = parse_ack(sock.recv(PACKET_SIZE))
                if not ack_fields:
                    raise ValueError(
                        "Received invalid response from server. Closing connection..."
                    )
                # Report any errors from the server
                elif ack_fields["status"] == "1":
                    raise Exception(ack_fields["msg"])

                if (type == "get"):
                    receive_file(sock, packets_needed(
                        server_qualify, arg), client_qualify(arg))
                elif (type == "put"):
                    send_file(sock, packets_needed(
                        client_qualify, arg), client_qualify(arg))
                elif (type == "list"):
                    receive_list(sock)
                else:
                    print("unknown command type")

                request_details = make_request_details(
                    ip, port, type, arg if type != "list" else "N/A", int(ack_fields["status"]))
                print(report(request_details))
        return with_arg

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


def to_request(request_name: str) -> int:
    status_dict = {"get": 0, "put": 1, "list": 2}
    return status_dict[request_name]


def main():
    REQUEST_TYPES = ("get", "put", "list")

    try:
        make_directory("client_files")
    except (FileExistsError):
        pass
    args = get_args()
    request_of = make_requester(args["ip"], args["port"])
    commands = {t: request_of(t) for t in REQUEST_TYPES}

    for k in commands:
        # NOTE: empty file paths will fall through this (on purpose)
        if args[k] is not None:
            print("Executing command")
            # try:
            return commands[k](args[k])

            # except Exception as e:
            #     return print(str(e))

    # No request made
    print(
        "Error: You must make a request with --get, --put, or --list. See --help for more info"
    )


if __name__ == "__main__":
    main()
