import os
import secrets
from subprocess import call
from factioncli.processing.cli import log
from factioncli.processing.config import get_config
from factioncli.processing.cli.printing import print_output, error_out
from factioncli.processing.docker.container import get_container, execute_container_command


def _cleanup_build_artifacts(container_name='faction_core_1'):
    print_output("Cleaning build artifacts from Core..")
    core = get_container(container_name)
    bin_result = execute_container_command(core, 'rm -rf /app/bin')
    obj_result = execute_container_command(core, 'rm -rf /app/obj')
    success = True
    if bin_result.exit_code != 0:
        error_out("Could not clean up build artifacts. Output from rm -rf /app/bin: \n{0}".format(bin_result.output))
        success = False
    if bin_result.exit_code != 0 or obj_result.exit_code != 0:
        error_out("Could not clean up build artifacts. Output from rm -rf /app/obj: \n{0}".format(obj_result.output))
        success = False
    if success:
        print_output("Migration created.")
        

def create_database_migration(name, container_name='faction_core_1'):
    _cleanup_build_artifacts()
    print_output("Creating database migration..")
    core = get_container(container_name)
    name = name + "_" + secrets.token_hex(8)
    result = execute_container_command(core, 'dotnet ef migrations add {0}'.format(name))
    if result.exit_code != 0:
        error_out("Could create migration. Output from command: \n{0}".format(result.output))
    else:
        print_output("Migration created.")


def drop_database(container_name='faction_core_1'):
    print_output("Dropping database..")
    core = get_container(container_name)
    result = execute_container_command(core, 'dotnet ef database drop --force')
    if result.exit_code != 0:
        error_out("Could not drop database. Output from command: \n{0}".format(result.output))
    else:
        print_output("Database dropped.")


def update_database(container_name='faction_core_1'):
    print_output("Updating database..")
    core = get_container(container_name)
    result = execute_container_command(core, 'dotnet ef database update')
    if result.exit_code != 0:
        error_out("Could not update database. Output from command: \n{0}".format(result.output))
    else:
        print_output("Database updated.")


def remove_database_files():
    print_output("Removing database files..")
    config = get_config()
    install_path = os.path.join(config["FACTION_PATH"], "install/")
    data_path = os.path.join(config["FACTION_PATH"], "data/")
    command = "sudo su -c 'rm -rf {0}*'".format(data_path)
    log.debug("Running: '{0}' from {1}".format(command, install_path))
    call(command, cwd=install_path, shell=True)
