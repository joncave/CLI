from factionpy.processing.user_role import create_role
from factioncli.processing.cli.printing import print_output


def create_faction_roles(roles=("system", "admin", "operator", "readonly")):
    print_output("Creating Faction Roles..")
    for role in roles:
        create_role(role)
