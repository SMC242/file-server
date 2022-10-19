import socket
from dataclasses import dataclass
from enum import Enum

# Remove these later - they're for strong typing during development
class CommandType(Enum):
    GET = "get"
    PUT = "put"
    LIST = "list"


class Status(Enum):
    SUCCESS = 0
    FAILURE = 1


@dataclass
class CommandDetails:
    ip: str
    port: int
    type: CommandType
    status: Status


def report(details: CommandDetails) -> str:
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
