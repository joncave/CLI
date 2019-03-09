import logging
from cliff.lister import Lister
from factioncli.processing.cli.printing import error_out
from factioncli.processing.config import get_config
from factioncli.processing.status.containers import get_container_status


class Status(Lister):
    "Checks if your Faction is feeling ok"

    def take_action(self, parsed_args):
        config = get_config()
        containers = config["CONTAINERS"]
        results = []
        for container in containers:
            status = get_container_status(container)
            if status:
                results.append((status.name, status.status, status.ip_address, status.created))
            else:
                error_out("Container {0} not found. Faction won't work with out this.".format(container))
        return (("Container Name", "Status", "IP Address", "Created"), results)