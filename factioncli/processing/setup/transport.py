from factioncli.backend.database import FactionDB
from factioncli.processing.cli import log
from factioncli.processing.cli.printing import error_out, print_output
from factioncli.processing.config import get_config


def create_transport(name, description, guid, api_key_id, configuration):
    faction_db = FactionDB()
    print_output("Creating Transport: {0}".format(name))
    log.debug("Description: {0}".format(description))
    log.debug("Guid: {0}".format(guid))
    log.debug("API Key ID: {0}".format(api_key_id))
    log.debug("Configuration: {0}".format(configuration))
    faction_db.session.add(faction_db.Transport(Name=name,
                          Description=description,
                          Guid=guid,
                          ApiKeyId=api_key_id,
                          Configuration=configuration,
                          Enabled=True,
                          Visible=True))
    faction_db.session.commit()


def create_direct_transport(name="DIRECT", description="DIRECT Transport", guid="0000-0000-0000-0000-0000", api_key=None):
    config = get_config()
    if not api_key:
        error_out("No API Key included in request")

    configuration = '{"ApiUrl":"' + config['EXTERNAL_ADDRESS'] + '","ApiKeyName":"' + api_key['Name'] + '","ApiSecret":"' + api_key['Token'] +'"}'
    create_transport(name, description, guid, api_key["Id"], configuration)