import os
from subprocess import call

from factioncli.processing.cli import log
from factioncli.processing.cli.printing import print_output, error_out
from factioncli.processing.config import get_config


def remove_agenttype_files():
    print_output("Removing agent type files..")
    config = get_config()
    agent_path = os.path.join(config["FACTION_PATH"], "agents/")
    build_path = os.path.join(config["FACTION_PATH"], "agents/build")
    command = "sudo su -c 'rm -rf {0}*'".format(agent_path)
    log.debug("Running: '{0}' from {1}".format(command, os.path.join(config["FACTION_PATH"])))
    call(command, cwd=os.path.join(config["FACTION_PATH"]), shell=True)
    create_build_command = "sudo su -c 'mkdir -p {0}'".format(build_path)
    log.debug("Running: '{0}' from {1}".format(create_build_command, os.path.join(config["FACTION_PATH"])))
    call(create_build_command, cwd=os.path.join(config["FACTION_PATH"]), shell=True)


def remove_builds():
    print_output("Removing agent build files..")
    config = get_config()
    build_path = os.path.join(config["FACTION_PATH"], "agents/build")
    command = "sudo su -c 'rm -rf {0}*'".format(build_path)
    log.debug("Running: '{0}' from {1}".format(command, os.path.join(config["FACTION_PATH"])))
    call(command, cwd=os.path.join(config["FACTION_PATH"]), shell=True)


def remove_modules():
    print_output("Removing modules..")
    config = get_config()
    modules_path = os.path.join(config["FACTION_PATH"], "modules/")
    command = "sudo su -c 'rm -rf {0}*'".format(modules_path)
    log.debug("Running: '{0}' from {1}".format(command, os.path.join(config["FACTION_PATH"])))
    call(command, cwd=os.path.join(config["FACTION_PATH"]), shell=True)


def remove_uploads():
    print_output("Removing uploaded files..")
    config = get_config()
    paths = []
    uploads_path = os.path.join(config["FACTION_PATH"], "uploads/")
    paths.append(os.path.join(uploads_path, "files/"))
    paths.append(os.path.join(uploads_path, "payloads/"))
    for path in paths:
        command = "sudo su -c 'rm -rf {0}*'".format(path)
        log.debug("Running: '{0}' from {1}".format(command, uploads_path))
        call(command, cwd=uploads_path, shell=True)
