from factioncli.backend.database import FactionDB
from factioncli.processing.cli import log
from factioncli.processing.cli.printing import error_out, print_output


def create_role(name):
    print_output("In create_role, creating FactionDB..")
    faction_db = FactionDB()
    print_output("Creating UserRole: {0}".format(name))
    faction_db.session.add(faction_db.UserRole(Name=name.lower()))
    faction_db.session.commit()


def get_role_id(name):
    faction_db = FactionDB()
    log.debug("Getting ID for role: {0}".format(name))
    role = faction_db.session.query(faction_db.UserRole).filter_by(Name=name.lower()).first()
    if role:
        log.debug("Got UserRole ID: {0}".format(role.Id))
        return role.Id
    else:
        error_out("Could not find role named: {0}".format(name))


def create_faction_roles(roles=("system", "admin", "operator", "readonly")):
    print_output("In create_faction_roles")
    for role in roles:
        print_output("Running create_role({0})".format(role))
        create_role(role)
