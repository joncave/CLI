from cliff.lister import Lister
from factioncli.processing.config import get_passwords


class Credentials(Lister):
    "Returns a list of the default credentials for this instance of Faction"

    def take_action(self, parsed_args):
        passwords = get_passwords()
        return ("Type", "Username", "Password"), passwords
