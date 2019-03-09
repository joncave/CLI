from datetime import datetime
from factioncli.processing.cli import log

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def current_time():
    return datetime.now().strftime("%H:%M:%S")

def print_output(message):
    print("{0}[{1}] {2}{3}".format(bcolors.OKGREEN, current_time(), message, bcolors.ENDC))

def error_out(message, status=1):
    log.error("{0}{1}{2}".format(bcolors.FAIL, message, bcolors.ENDC))
    exit(status)