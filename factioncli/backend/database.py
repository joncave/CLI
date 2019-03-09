from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from factioncli.processing.config import get_config
from factioncli.processing.docker import get_container_ip_address

class FactionDB:
    User = None
    UserRole = None
    Transport = None
    ApiKey = None
    base = None
    engine = None
    session = None

    def __init__(self):
        CONFIG = get_config()
        db_params = {'drivername': 'postgres',
                  'username': CONFIG['POSTGRES_USERNAME'],
                  'password': CONFIG['POSTGRES_PASSWORD'],
                  'host': get_container_ip_address("faction_db_1"),
                 'database': CONFIG['POSTGRES_DATABASE']
                  }

        db_url = URL(**db_params)
        self.engine = create_engine(db_url)
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)

        self.User = self.base.classes.User
        self.UserRole = self.base.classes.UserRole
        self.Transport = self.base.classes.Transport
        self.ApiKey = self.base.classes.ApiKey

    def close(self):
        self.session.close()