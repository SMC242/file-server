from argparse import ArgumentParser


def request(type: str) -> None:
    pass


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


def main():
    REQUEST_TYPES = ("get", "put", "list")
    COMMANDS = {
        "get": lambda: request("get"),
        "put": lambda: request("put"),
        "list": lambda: request("list"),
    }
    args = get_args()
    for k in COMMANDS:
        # NOTE: empty file paths will fall through this (on purpose)
        if args[k]:
            print("executing")
            return COMMANDS[k]()

    # No request made
    print(
        "Error: You must make a request with --get, --put, or --list. See --help for more info"
    )


if __name__ == "__main__":
    main()
