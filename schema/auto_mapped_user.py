from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import os
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
engine = create_engine(os.environ["DEV_DATABASE_URI"])

session = Session(engine)

# produce our own MetaData object
metadata = MetaData()

# we can reflect it ourselves from a database, using options
# such as 'only' to limit what tables we look at...
metadata.reflect(engine)

# ... or just define our own Table objects with it (or combine both)
# Table('user_order', metadata,
#       Column('id', Integer, primary_key=True),
#       Column('user_id', ForeignKey('user.id'))
#       )

# we can then produce a set of mappings from this MetaData.
Base = automap_base(metadata=metadata)

# calling prepare() just sets up mapped classes and relationships.
Base.prepare()


# mapped classes are ready
User, Settings, Investigator = Base.classes.PiptUser(SQLAlchemyObjectType), Base.classes.PiptUserSetting, Base.classes.Investigator


lol = "got this thing"
