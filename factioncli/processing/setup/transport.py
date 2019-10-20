from factionpy.processing.transport import create_transport
from factioncli.processing.cli.printing import error_out, print_output
from factioncli.processing.config import get_config


def create_direct_transport(name="DIRECT Transport", transport_type="DIRECT", guid="0000-0000-0000-0000-0000",
                            api_key=None):
    print_output("Creating {0}".format(name))
    config = get_config()
    if not api_key:
        error_out("No API Key included in request")

    configuration = '{"TransportId": 1, "ApiUrl":"' + config['EXTERNAL_ADDRESS'] + '","ApiKeyName":"' + api_key[
        'Name'] + '","ApiSecret":"' + api_key['Token'] + '"}'
    create_transport(name, transport_type, guid, api_key["Id"], configuration)
