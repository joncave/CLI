import logging
from cliff.command import Command
from factioncli.processing.setup.user import get_user_id
from factioncli.processing.cli.printing import print_output
from factioncli.processing.setup.api_key import create_api_key


class New(Command):
    "Create new stuff"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(New, self).get_parser(prog_name)
        parser.add_argument('--transport-key',
                            help="Create a new transport key",
                            action="store_true")
        return parser

    def take_action(self, parsed_args):
        if parsed_args.transport_key:
            system_id = get_user_id('system')
            api_key = create_api_key(user_id=system_id, owner_id=system_id, type="Transport")
            print_output("Transport API Key Created.\n\nKey Name: {0}\nSecret: {1}".format(api_key["Name"], api_key["Token"]))
