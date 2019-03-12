import logging
from cliff.command import Command
from factioncli.processing.cli.printing import print_output
from factioncli.processing.faction.control import clean_faction
from factioncli.processing.faction.database import remove_database_files
from factioncli.processing.faction.filesystem import remove_agenttype_files, remove_uploads


class Clean(Command):
    "Clean Faction data and containers"

    def get_parser(self, prog_name):
        parser = super(Clean, self).get_parser(prog_name)
        parser.add_argument('--all',
                            help="Remove Faction containers, Database, Generated Files, and Uploads",
                            action="store_true")
        parser.add_argument('--faction',
                            help="Remove Faction containers",
                            action="store_true")
        parser.add_argument('--database',
                            help="Remove Faction database files",
                            action="store_true")
        parser.add_argument('--agent-types',
                            help="Remove built agent types and built payloads",
                            action="store_true")
        parser.add_argument('--uploads',
                            help="Remove files and payloads that have been uploaded to Faction",
                            action="store_true")
        return parser

    def take_action(self, parsed_args):
        if parsed_args.database or parsed_args.all:
            remove_database_files()

        if parsed_args.faction or parsed_args.all:
            clean_faction()

        if parsed_args.agent_types or parsed_args.all:
            remove_agenttype_files()

        if parsed_args.uploads or parsed_args.all:
            remove_uploads()

