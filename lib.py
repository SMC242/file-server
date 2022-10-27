import socket
import os
from math import ceil

from request import make_list, parse_list, to_fields

# 1 KiB
PACKET_SIZE = 1024


def make_request_details(
    ip: str, port: int, type: str, file_name: str | None, status: int
) -> dict:
    """Use this instead of the RequestDetails constructor to make removing it easier"""
    return {"ip": ip, "port": port, "request_type": type, "file_name": file_name, "status": status}


def report(details: dict) -> str:
    report_string = generate_report(details)
    return report_string


def generate_report(report_dict: dict) -> str:
    report_string = ""
    for key, value in report_dict.items():
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


def send_file(socket: socket.socket, packets: int, file_path: str) -> None:
    try:
        with open(file_path, "rb") as f:
            for i in range(packets):
                # read a packet of data at a time
                byte_array = f.read(PACKET_SIZE)
                socket.sendall(byte_array)
    except (FileNotFoundError):
        print("file not found")


def receive_file(socket: socket.socket, packets: int, out_path: str) -> None:
    try:
        with open(out_path, "xb") as f:
            for _ in range(packets):
                received_bytes = socket.recv(PACKET_SIZE)
                f.write(received_bytes)
    except (FileExistsError):
        print("file already exists, cannot overwrite")


def make_qualifier(dir: str):
    def qualify(name: str) -> str:
        """Prefix the file path with `files/` to avoid cluttering `/`"""
        return f"./{dir}/{name}"

    return qualify


def list_files(qualifier) -> list[str]:
    return os.listdir(qualifier(""))


def partition(n: int, xs) -> list:
    """Return a list of slices of size `n`"""
    return [xs[i: i + n] for i in range(0, len(xs), n)]


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
    for _ in range(int(fields["n"])):
        buffer += socket.recv(PACKET_SIZE)

    files = parse_list(buffer.decode("utf-8"))
    print(f"Available files:\n {format_list(files)}")


def format_list(xs: list[str]) -> str:
    return_string = ""
    for item in xs:
        return_string += item + ",\n"

    return return_string


def valid_file(qualifier, name: str) -> bool:
    qualified = qualifier(name)
    return os.path.exists(qualified) and os.path.isfile(qualified)


def packets_needed(qualifier, file_name: str) -> int:
    return ceil(os.stat(qualifier(file_name)).st_size / PACKET_SIZE)


def make_directory(name: str) -> None:
    os.makedirs(name)


if __name__ == "__main__":
    pass
