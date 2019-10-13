from factionpy.backend.database import db
from factionpy.models.transport import Transport

from factioncli.processing.cli import log
from factioncli.processing.cli.printing import error_out, print_output
from factioncli.processing.config import get_config


def create_transport(name, transport_type, guid, api_key_id, configuration):
    print_output("Creating Transport: {0}".format(name))
    log.debug("Transport Type: {0}".format(transport_type))
    log.debug("Guid: {0}".format(guid))
    log.debug("API Key ID: {0}".format(api_key_id))
    log.debug("Configuration: {0}".format(configuration))
    db.session.add(Transport(Name=name,
                             TransportType=transport_type,
                             Guid=guid,
                             ApiKeyId=api_key_id,
                             Configuration=configuration,
                             Enabled=True,
                             Visible=True))
    db.session.commit()


def create_direct_transport(name="DIRECT Transport", transport_type="DIRECT", guid="0000-0000-0000-0000-0000",
                            api_key=None):
    config = get_config()
    if not api_key:
        error_out("No API Key included in request")

    configuration = '{"TransportId": 1, "ApiUrl":"' + config['EXTERNAL_ADDRESS'] + '","ApiKeyName":"' + api_key[
        'Name'] + '","ApiSecret":"' + api_key['Token'] + '"}'
    create_transport(name, transport_type, guid, api_key["Id"], configuration)
