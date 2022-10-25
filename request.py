"""
This module handles formatting and parsing requests
"""


def make_inital_req(type: int, name: str, n: int) -> str:
    return f"{type=} {name=} {n=}"


def make_ack(status: int, msg: str, n: int) -> str:
    return f"{status=} {msg=} {n=}"


def make_list(file_names: list[str]) -> str:
    return " ".join(file_names)


def to_fields(msg: str) -> dict:
    """Convert a message to its fields. Use `parse_list` for list responses"""
    split = msg.split(" ")
    return {f[0]: f[1] for f in map(lambda s: s.split("="), split)}


def parse_list(list_response: str) -> list[str]:
    return list_response.split(" ")


def validate(keys: list[str]):
    """Get a functon to check if a response had the correct fields"""

    def inner(fields: dict) -> bool:
        return all(k in fields for k in keys)

    return inner


def validate_type(type: str | int) -> bool:  # Ducks say quack o7
    return type in {0, 1, 2, "0", "1", "2"}


validate_initial = validate(["type", "name", "n"])
validate_ack = validate(["status", "msg", "n"])
