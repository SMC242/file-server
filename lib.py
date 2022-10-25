import socket
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias
import os
from math import ceil

from request import make_list, parse_list, to_fields

# 1 KiB
PACKET_SIZE = 1024

FormattedAddress: TypeAlias = str  # !TODO: remove before submitting

# !TODO: remove before submitting
class RequestType(Enum):
    GET = 0
    PUT = 1
    LIST = 2


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1


@dataclass
class RequestDetails:
    ip: str
    port: int
    type: RequestType
    file_name: str | None
    status: Status


def make_request_details(
    ip: str, port: int, type: int, file_name: str | None, status: int
) -> RequestDetails:
    """Use this instead of the RequestDetails constructor to make removing it easier"""
    return RequestDetails(ip, port, RequestType(type), file_name, Status(status))


def report(details: RequestDetails) -> str:
    pass


def send_file(socket: socket.socket, packets: int, file_name: str) -> None:
    pass


def receive_file(socket: socket.socket, packets: int, out_path: str) -> None:
    pass


def qualify(name: str) -> str:
    """Prefix the file path with `files/` to avoid cluttering `/`"""
    return f"./files/{name}"


def list_files() -> list[str]:
    return os.listdir(qualify(""))


def partition(n: int, xs) -> list:
    """Return a list of slices of size `n`"""
    return [xs[i : i + n] for i in range(0, len(xs), n)]


def send_list(socket: socket.socket, files: list[str]) -> None:
    as_bytes = make_list(files).encode("utf-8")
    chunks = partition(PACKET_SIZE, as_bytes)
    socket.sendall(f"n={len(chunks)}".encode("utf-8"))
    for c in chunks:
        socket.sendall(c)


def receive_list(socket: socket.socket) -> None:
    fields = to_fields(socket.recv(PACKET_SIZE).decode("utf-8"))
    if not fields or not fields.get("n"):
        raise RuntimeError("Error during transmission")

    buffer = b""
    for _ in range(fields["n"]):
        buffer += socket.recv(PACKET_SIZE)

    files = parse_list(buffer.decode("utf-8"))
    print(f"Available files: {files}")


def format_address(ip: str, port: int) -> FormattedAddress:
    return f"{ip}:{port}"


def valid_file(name: str) -> bool:
    qualified = qualify(name)
    return os.path.exists(qualified) and os.path.isfile(qualified)


def packets_needed(file_name: str) -> int:
    return ceil(os.stat(file_name).st_size / PACKET_SIZE)
