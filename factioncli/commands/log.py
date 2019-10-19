import logging
from cliff.command import Command
from factioncli.processing.docker.logs import get_logs


class Log(Command):
    "Handles Log Command"

    def get_parser(self, prog_name):
        parser = super(Log, self).get_parser(prog_name)
        parser.add_argument('-f','--follow',
                            help="Enable log following",
                            action="store_true")
        parser.add_argument('--container',
                            help="Target container name",
                            action="store",
                            nargs=1)
        
        return parser
    
    def take_action(self, parsed_args):
        get_logs(parsed_args.container, parsed_args.follow)