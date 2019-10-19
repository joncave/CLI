import os
from subprocess import call
from factioncli.processing.cli import log
from factioncli.processing.cli.printing import print_output, error_out
from factioncli.processing.config import get_config


def clean_faction():
    print_output("Removing Faction Docker Containers and Images..")
    config = get_config()
    install_path = os.path.join(config["FACTION_PATH"], "install/")
    log.debug("Running: 'docker-compose -p faction down --remove-orphans --rmi all' from {0}".format(install_path))
    call("docker-compose -p faction down --remove-orphans --rmi all", cwd=install_path, shell=True)


def build_faction():
    print_output("Building Faction containers..")
    try:
        config = get_config()
        install_path = os.path.join(config["FACTION_PATH"], "install/")
        log.debug("Running: 'docker-compose -p faction up -d --force-recreate --build' from {0}".format(install_path))
        ret = call("docker-compose -p faction up -d --force-recreate --build", cwd=install_path, shell=True)
        if ret == 0:
            print_output("Faction has been built")
        else:
            error_out("Failed to build Faction.")
    except Exception as e:
        error_out("Building Faction failed. Error: {0}".format(str(e)))


def start_faction():
    print_output("Starting Faction..")
    config = get_config()
    install_path = os.path.join(config["FACTION_PATH"], "install/")
    log.debug("Running: 'docker-compose -p faction start' from {0}".format(install_path))
    call("docker-compose -p faction start", cwd=install_path, shell=True)


def stop_faction():
    print_output("Stopping Faction..")
    config = get_config()
    install_path = os.path.join(config["FACTION_PATH"], "install/")
    log.debug("Running: 'docker-compose -p faction stop' from {0}".format(install_path))
    call("docker-compose -p faction stop", cwd=install_path, shell=True)
