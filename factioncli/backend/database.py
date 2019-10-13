from sqlalchemy.ext.automap import automap_base, generate_relationship, name_for_collection_relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Integer, Column
from sqlalchemy.engine.url import URL
from factioncli.processing.config import get_config
from factioncli.processing.docker.container import get_container_ip_address
from factioncli.processing.cli.printing import print_output


class FactionDB:
    User = None
    UserRole = None
    Transport = None
    ApiKey = None
    base = None
    engine = None
    session = None

    def __init__(self):
        print_output("FactionDB: Pulling Config")
        CONFIG = get_config()
        db_params = {'drivername': 'postgres',
                     'username': CONFIG['POSTGRES_USERNAME'],
                     'password': CONFIG['POSTGRES_PASSWORD'],
                     'host': get_container_ip_address("faction_db_1"),
                     'database': CONFIG['POSTGRES_DATABASE']
                     }

        # Resolves an issue with backrefs, thanks to this stackoverflow user for answering
        # their own question: https://stackoverflow.com/a/49515079
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

        print_output("FactionDB: Assigning db_url")
        db_url = URL(**db_params)
        print_output("FactionDB: Assigning engine")
        self.engine = create_engine(db_url)
        print_output("FactionDB: Assigning base")
        self.base = automap_base()

        print_output("FactionDB: Seeding tables with Id stuff")

        class User(self.base):
            __tablename__ = "User"
            # Override id column, the type must match. Automap handles the rest.
            Id = Column(Integer, primary_key=True)

        class UserRole(self.base):
            __tablename__ = "UserRole"
            # Override id column, the type must match. Automap handles the rest.
            Id = Column(Integer, primary_key=True)

        class Agent(self.base):
            __tablename__ = "Agent"
            # Override id column, the type must match. Automap handles the rest.
            Id = Column(Integer, primary_key=True)

        class Transport(self.base):
            __tablename__ = "Transport"
            # Override id column, the type must match. Automap handles the rest.
            Id = Column(Integer, primary_key=True)

        class ApiKey(self.base):
            __tablename__ = "ApiKey"
            # Override id column, the type must match. Automap handles the rest.
            Id = Column(Integer, primary_key=True)

        print_output("FactionDB: Running base.prepare()")
        self.base.prepare(self.engine,
                          reflect=True,
                          generate_relationship=_gen_relationship,
                          name_for_collection_relationship=_name_for_collection_relationship)
        print_output("FactionDB: Assigning session")
        self.session = Session(self.engine)

        print_output("FactionDB: Assigning User")
        self.User = self.base.classes.User
        print_output("FactionDB: Assigning UserRole")
        self.UserRole = self.base.classes.UserRole
        print_output("FactionDB: Assigning Agent")
        self.Agent = self.base.classes.Agent
        print_output("FactionDB: Assigning Transport")
        self.Transport = self.base.classes.Transport
        print_output("FactionDB: Assigning ApiKey")
        self.ApiKey = self.base.classes.ApiKey

    def close(self):
        self.session.close()
