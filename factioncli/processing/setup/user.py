import bcrypt
from datetime import datetime
from factioncli.backend.database import FactionDB
from factioncli.processing.cli import log
from factioncli.processing.cli.printing import error_out, print_output
from factioncli.processing.config import get_config
from factioncli.processing.setup.user_role import get_role_id

def create_user(username, password, role_id):
    faction_db = FactionDB()
    print_output("Creating User: {0}".format(username))
    log.debug("Password: {0}".format(password))
    log.debug("User Role ID: {0}".format(role_id))
    faction_db.session.add(faction_db.User(Username=username,
         Password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
         Created=datetime.utcnow(),
         RoleId=role_id,
         Enabled = True,
         Visible = True))
    faction_db.session.commit()

def get_user_id(username):
    faction_db = FactionDB()
    log.debug("Getting ID for User: {0}".format(username))
    user = faction_db.session.query(faction_db.User).filter_by(Username=username.lower()).first()
    if user:
        log.debug("Got User ID: {0}".format(user.Id))
        return user.Id
    else:
        error_out("Could not find user named: {0}".format(username))

def create_admin_user(admin_username=None, admin_password=None):
    if not admin_username:
        config = get_config()
        admin_username = config['ADMIN_USERNAME']

    if not admin_password:
        config = get_config()
        admin_password = config['ADMIN_PASSWORD']

    if not len(admin_username) > 0 or not len(admin_password) > 0:
        error_out("Admin Username and/or Admin Password not found in config. Run `setup` to initialize faction or `new config` to create a new config")
    create_user(admin_username, admin_password, get_role_id("admin"))


def create_system_user(system_username=None, system_password=None):
    if not system_username:
        config = get_config()
        system_username = config['SYSTEM_USERNAME']

    if not system_password:
        config = get_config()
        system_password = config['SYSTEM_PASSWORD']
    if not len(system_username) > 0 or not len(system_password) > 0:
        error_out("System Username and/or System Password not found in config. Run `setup` to initialize Faction or `new config` to create a new config")
    create_user(system_username, system_password, get_role_id("system"))
