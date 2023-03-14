class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\u001b[36m'
    WARNING = '\u001b[31;1m'
    YELLOW = '\u001b[33;1m'
    ENDC = '\033[0m'    

def print_header(msg) -> None:
    _print(bcolors.HEADER + msg + bcolors.ENDC)

def print_info(msg) -> None:
    _print(bcolors.OKBLUE + msg + bcolors.ENDC)

def print_debug(msg) -> None:
    _print(msg)

def print_warning(msg) -> None:
    _print(bcolors.YELLOW + msg + bcolors.ENDC)

def print_error(msg) -> None:
    _print(bcolors.WARNING + msg + bcolors.ENDC)

def _print(msg) -> None:
    print(msg, flush=True)