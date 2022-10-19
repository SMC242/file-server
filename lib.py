import socket
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

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
    type: CommandType
    file_name: str | None
    status: Status


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
