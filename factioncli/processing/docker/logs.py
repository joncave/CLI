import logging
import os
from subprocess import call
from factioncli.processing.config import get_config
from factioncli.processing.cli import log


def get_logs(container_name=None, follow=False):
    config = get_config()
    install_path = os.path.join(config["FACTION_PATH"], "install/")

    if follow:
        compose_command = 'docker-compose -p faction logs --follow {0}'.format(container_name)
    else:
        compose_command = 'docker-compose -p faction logs {0}'.format(container_name)

    log.debug("Running {0} from {1}".format(compose_command, install_path))

    call(compose_command, cwd=install_path, shell=True)
