import logging
from cliff.command import Command
from factioncli.processing.faction.control import start_faction, stop_faction, clean_faction, build_faction


class Start(Command):
    "Starts Faction Services"

    def take_action(self, parsed_args):
        start_faction()


class Stop(Command):
    "Stops Faction Services"

    def take_action(self, parsed_args):
        stop_faction()


class Restart(Command):
    "Restarts Faction Services"

    def take_action(self, parsed_args):
        stop_faction()
        start_faction()


class Reset(Command):
    "Resets Faction to a fresh install"

    def take_action(self, parsed_args):
        clean_faction()
        build_faction()
