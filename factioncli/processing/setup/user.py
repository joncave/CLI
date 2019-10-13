from factionpy.processing.user import create_user
from factionpy.processing.user_role import get_role_id
from factioncli.processing.cli.printing import error_out
from factioncli.processing.config import get_config


def create_admin_user(admin_username=None, admin_password=None):
    if not admin_username:
        config = get_config()
        admin_username = config['ADMIN_USERNAME']

    if not admin_password:
        config = get_config()
        admin_password = config['ADMIN_PASSWORD']

    if not len(admin_username) > 0 or not len(admin_password) > 0:
        error_out(
            "Admin Username and/or Admin Password not found in config. Run `setup` to initialize faction or `new "
            "config` to create a new config")
    create_user(admin_username, admin_password, get_role_id("admin"))


def create_system_user(system_username=None, system_password=None):
    if not system_username:
        config = get_config()
        system_username = config['SYSTEM_USERNAME']

    if not system_password:
        config = get_config()
        system_password = config['SYSTEM_PASSWORD']
    if not len(system_username) > 0 or not len(system_password) > 0:
        error_out(
            "System Username and/or System Password not found in config. Run `setup` to initialize Faction or `new "
            "config` to create a new config")
    create_user(system_username, system_password, get_role_id("system"))
