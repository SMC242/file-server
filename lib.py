import socket
from dataclasses import dataclass, asdict
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
    report_string = report_string.strip()
    if report_string[-1] == ",":  # remove last comma
        report_string = report_string[:-1]
    return report_string


def send_file(
    socket: socket.socket, packets: int, file_name: str
) -> None:
    try:
        with open(file_name, "rb") as f:
            for i in range(packets):
                # read a packet of data at a time
                byte_array = f.read(PACKET_SIZE)
                socket.sendall(byte_array)
    except (FileNotFoundError):
        print("file not found")


def receive_file(
    socket: socket.socket, packets: int, out_path: str
) -> None:
    try:
        with open(out_path, "xb") as f:
            for i in range(packets):
                received_btyes = socket.recv(PACKET_SIZE)
                f.write(received_btyes)
    except (FileExistsError):
        print("file already exists, cannot overwrite")


def qualify(name: str) -> str:
    """Prefix the file path with `files/` to avoid cluttering `/`"""
    return f"./files/{name}"


def list_files() -> list[str]:
    return os.listdir(qualify(""))


def send_list(socket: socket.socket, files: list[str]) -> None:
    file_list_bytes = ",".join(files).encode("utf-8")
    socket.send(file_list_bytes)


def receive_list(socket: socket.socket) -> None:
    list_as_string = socket.recv(PACKET_SIZE).decode("utf-8")
    file_list = list_as_string.split(',')
    print_list(file_list)


def print_list(list: list[str]) -> None:
    for i in list:
        print(i)


def format_address(ip: str, port: int) -> FormattedAddress:
    return f"{ip}:{port}"


def valid_file(name: str) -> bool:
    qualified = qualify(name)
    return os.path.exists(qualified) and os.path.isfile(qualified)


def packets_needed(file_name: str) -> int:
    return ceil(os.stat(file_name).st_size / PACKET_SIZE)


if __name__ == "__main__":
    pass
