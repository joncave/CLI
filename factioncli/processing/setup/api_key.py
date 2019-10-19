import bcrypt
import secrets
from datetime import datetime
from factioncli.processing.cli.printing import print_output
from factionpy.processing.api_key import new_api_key


def create_api_key(user_id, owner_id, api_key_type):

    print_output("Creating API Key with type: {0}".format(api_key_type))
    key = new_api_key(api_key_type=api_key_type, user_id=user_id, owner_id=owner_id)

    return dict({
        "Id": key.Id,
        "Name": key.Name,
        "Token": key.Token
    })
