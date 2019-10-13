from factionpy.processing.user_role import create_role
from factioncli.processing.cli.printing import print_output


def create_faction_roles(roles=("system", "admin", "operator", "readonly")):
    print_output("In create_faction_roles")
    for role in roles:
        print_output("Running create_role({0})".format(role))
        create_role(role)
