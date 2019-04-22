from sqlalchemy.ext.automap import automap_base, generate_relationship, name_for_collection_relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from factioncli.processing.config import get_config
from factioncli.processing.docker.container import get_container_ip_address

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

        # Resolves an issue with backrefs, thanks to this stackoverflow
        # user for answering their own question: https://stackoverflow.com/a/49515079
        def _gen_relationship(base, direction, return_fn,
                              attrname, local_cls, referred_cls, **kw):
            return generate_relationship(base, direction, return_fn,
                                         attrname + '_ref', local_cls, referred_cls, **kw)

        # this person seems to know what they're talking about: https://stackoverflow.com/a/48288656
        def _name_for_collection_relationship(base, local_cls, referred_cls, constraint):
            if constraint.name:
                return constraint.name.lower()
            # if this didn't work, revert to the default behavior
            return name_for_collection_relationship(base, local_cls, referred_cls, constraint)

        db_url = URL(**db_params)
        self.engine = create_engine(db_url)
        self.base = automap_base()
        self.base.prepare(self.engine,
                          reflect=True,
                          generate_relationship=_gen_relationship,
                          name_for_collection_relationship=_name_for_collection_relationship)
        self.session = Session(self.engine)

        self.User = self.base.classes.User
        self.UserRole = self.base.classes.UserRole
        self.Agent = self.base.classes.Agent
        self.Transport = self.base.classes.Transport
        self.ApiKey = self.base.classes.ApiKey

    def close(self):
        self.session.close()