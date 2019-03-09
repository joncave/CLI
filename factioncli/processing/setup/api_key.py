import bcrypt
import secrets
from datetime import datetime
from factioncli.backend.database import FactionDB
from factioncli.processing.cli.printing import print_output

def create_api_key(user_id, owner_id, type):
    faction_db = FactionDB()

    print_output("Creating API Key with type: {0}".format(type))
    name = secrets.token_urlsafe(12)
    token = secrets.token_urlsafe(48)
    api_key = faction_db.ApiKey(Name=name,
                       Key=bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt()),
                       Created=datetime.utcnow(),
                       UserId=user_id,
                       OwnerId=owner_id,
                       Enabled=True,
                       Visible=True
                       )
    faction_db.session.add(api_key)
    faction_db.session.commit()

    return dict({
        "Id": api_key.Id,
        "Name": name,
        "Token": token
    })