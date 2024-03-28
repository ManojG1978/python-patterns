class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_info(message):
    print(f"{Colors.OKCYAN}{message}{Colors.ENDC}")


def print_warning(message):
    print(f"{Colors.WARNING}{message}{Colors.ENDC}")


def print_error(message):
    print(f"{Colors.FAIL}{message}{Colors.ENDC}")


def print_event(message):
    print(f"{Colors.OKCYAN}{message}{Colors.OKCYAN}")


def print_success(message):
    print(f"{Colors.OKGREEN}{message}{Colors.OKGREEN}")
