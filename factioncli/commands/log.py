import logging
from cliff.command import Command
from factioncli.processing.setup.user import get_user_id
from factioncli.processing.cli.printing import print_output
from factioncli.processing.setup.api_key import create_api_key

class Log(Command):
    "Handles Log Command"

    def get_parser(self, prog_name):
        parser = super(Clean, self).get_parser(prog_name)
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