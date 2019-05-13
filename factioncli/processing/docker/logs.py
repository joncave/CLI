import logging
from factioncli.processing.cli import log

def get_logs(container_name=None, follow=false):
    config = get_config()
    install_path = os.path.join(config["FACTION_PATH"], "install/")


    if follow == True:
        compose_command = 'docker-compose -p faction logs --follow {0}'.format(container_name)
    else:
        compose_command = 'docker-compose -p faction logs {0}'.format(container_name)

    log.debug(compose_command = " from {0}".format(install_path))

    call("docker-compose -p faction logs", cwd=install_path, shell=True)