from factioncli.processing.cli.printing import error_out
from factioncli.processing.docker import get_container

class container_status:
    name = ""
    status = ""
    ip_address = ""
    message = ""
    created = ""


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