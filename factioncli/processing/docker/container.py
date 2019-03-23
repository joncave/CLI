import logging
import docker
from docker.models.containers import Container

from factioncli.processing.cli import log
from factioncli.processing.cli.printing import error_out

client = docker.from_env()
class container_status:
    name = ""
    status = ""
    ip_address = ""
    message = ""
    created = ""

def get_container(container_name):
    log.debug("Searching for container named: {0}".format(container_name))
    containers = client.containers.list()
    for container in containers:
        if container.attrs['Name'] == "/{0}".format(container_name):
            return container
    log.debug("Could not find container named: {0}".format(container_name))
    return None

def get_container_ip_address(container_name, network_name='faction_default'):
    log.debug("Getting IP for container named {0} on network {1}".format(container_name, network_name))
    container = get_container(container_name)
    if container:
        return container.attrs["NetworkSettings"]["Networks"][network_name]['IPAddress']
    else:
        return None

def start_container(container):
    log.debug("Stopping container: {0}".format(container.attrs["Name"]))
    if isinstance(container, Container):
        if container.status == 'running':
            log.debug("Container {0} is not running. No need to stop it")
        else:
            container.start()
    else:
        error_out("{0} is not a container object".format(container))

def stop_container(container):
    log.debug("Stopping container: {0}".format(container.attrs["Name"]))
    if isinstance(container, Container):
        if container.status == 'running':
            container.stop()
        else:
            log.debug("Container {0} is not running. No need to stop it")
    else:
        error_out("{0} is not a container object".format(container))

def restart_container(container):
    log.debug("Stopping container: {0}".format(container.attrs["Name"]))
    if isinstance(container, Container):
        if container.status == 'running':
            container.restart()
        else:
            log.debug("Container {0} is not running. No need to stop it")
    else:
        error_out("{0} is not a container object".format(container))

def remove_container(container):
    log.debug("Stopping container: {0}".format(container.attrs["Name"]))
    if isinstance(container, Container):
        if container.status == 'running':
            container.stop()
        else:
            log.debug("Container {0} is not running. No need to stop it")
    else:
        error_out("{0} is not a container object".format(container))

def execute_container_command(container, command):
    log.debug("Executing {0} against container: {1}".format(command, container.attrs["Name"]))
    if isinstance(container, Container):
        if container.status == 'running':
            return container.exec_run(command)
        else:
            error_out("Container {0} is not running. Can not execute commands against it")
    error_out("{0} is not a container object".format(container))


def get_container_status(container_name, network_name='faction_default'):
    container = get_container(container_name)
    if container:
        status = container_status
        container_name = container.attrs["Name"]
        if container_name[0] == "/":
            container_name = container_name[1:]
        status.name = container_name
        status.status = container.status
        status.ip_address = container.attrs["NetworkSettings"]["Networks"][network_name]['IPAddress']
        status.created = container.attrs["Created"]
        return status