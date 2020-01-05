import logging
from datetime import datetime
from cliff.command import Command

from factionpy.processing.agent_type import new_agent_type
from factionpy.processing.user import get_user_id

from factioncli.processing.cli.printing import print_output
from factioncli.processing.setup.api_key import create_api_key


class New(Command):
    "Create new stuff Transports and Development Agents"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(New, self).get_parser(prog_name)
        parser.add_argument('--transport-key',
                            help="Create a new transport key",
                            action="store_true")
        parser.add_argument('--dev-agent',
                            help="Create a new development agent",
                            action="store_true")
        parser.add_argument('--name',
                            help="Name for the development agent")
        return parser

    def take_action(self, parsed_args):
        if parsed_args.transport_key:
            system_id = get_user_id('system')
            api_key = create_api_key(user_id=system_id, owner_id=system_id, type="Transport")
            print_output("Transport API Key Created.\n\nKey Name: {0}\nSecret: {1}".format(api_key["Name"], api_key["Token"]))
        elif parsed_args.dev_agent:
            if not parsed_args.name:
                name = datetime.utcnow().strftime("DEV-%Y%m%d%H%M%S")
            else:
                name = parsed_args.name
            agent_type = new_agent_type(name, name)
            print_output("New Development Agent created. \n\nName: {0}".format(agent_type.Name))