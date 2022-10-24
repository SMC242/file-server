import socket
from dataclasses import dataclass, asdict
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
    type: RequestType
    file_name: str | None
    status: Status


def make_request_details(
    ip: str, port: int, type: int, file_name: str | None, status: int
) -> RequestDetails:
    """Use this instead of the RequestDetails constructor to make removing it easier"""
    return RequestDetails(ip, port, RequestType(type), file_name, Status(status))


def report(details: RequestDetails) -> str:
    report_dict = asdict(details)
    report_string = generate_report(report_dict)
    return report_string


def generate_report(report_dict: dict) -> str:
    report_string = ""
    for key, value in report_dict.items():
        if isinstance(value, Enum):  # Enums need to be handled slightly differently
            report_string += append_report(key, str(value.name))
        else:
            report_string += append_report(key, str(value))
    report_string = clean_report_end(report_string)
    return report_string


def append_report(key: str, value: str):
    return f"{key}: {value}, "


def clean_report_end(report_string: str) -> str:
    report_string = report_string.strip()  # remove trailing whitespace
    if report_string[-1] == ',':  # remove last comma
        report_string = report_string[:-1]
    return report_string


def send_file(socket: socket.socket, file_name: str) -> None:  # TODO Taylor
    pass


def receive_file(socket: socket.socket) -> None:  # TODO Taylor
    pass


def list_files(path: str) -> list[str]:
    pass


def send_list(socket: socket.socket, files: list[str]) -> None:
    pass


def receive_list(socket: socket.socket) -> None:
    pass


def format_address(ip: str, port: int) -> FormattedAddress:
    return f"{ip}:{port}"


print(report(make_request_details("127.0.0.1", 65, 1, "test_output", 0)))
