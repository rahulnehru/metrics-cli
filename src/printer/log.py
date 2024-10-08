class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\u001b[36m'
    WARNING = '\u001b[31;1m'
    YELLOW = '\u001b[33;1m'
    ENDC = '\033[0m'


def print_header(msg) -> None:
    _print(Colors.HEADER + msg + Colors.ENDC)


def print_info(msg) -> None:
    _print(Colors.OKBLUE + f'\t{msg}' + Colors.ENDC)


def print_debug(msg) -> None:
    _print(f'\t\t{msg}')


def print_warning(msg) -> None:
    _print(Colors.YELLOW + f'\t{msg}' + Colors.ENDC)


def print_error(msg) -> None:
    _print(Colors.WARNING + msg + Colors.ENDC)


def br() -> None:
    _print('')


def _print(msg) -> None:
    print(msg, flush=True)
