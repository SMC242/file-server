import socket
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias
import os
from math import ceil

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


def send_file(socket: socket.socket, file_name: str) -> None:
    pass


def receive_file(socket: socket.socket) -> None:
    pass


def list_files(path: str) -> list[str]:
    pass


def send_list(socket: socket.socket, files: list[str]) -> None:
    pass


def receive_list(socket: socket.socket) -> None:
    pass


def format_address(ip: str, port: int) -> FormattedAddress:
    return f"{ip}:{port}"


def qualify(name: str) -> str:
    """Prefix the file path with `files/` to avoid cluttering `/`"""
    return f"./files/{name}"


def valid_file(name: str) -> bool:
    qualified = qualify(name)
    return os.path.exists(qualified) and os.path.isfile(qualified)


def packets_needed(file_name: str) -> int:
    return ceil(os.stat(file_name).st_size / PACKET_SIZE)
