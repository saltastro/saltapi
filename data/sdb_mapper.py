from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session

import os


def to_map(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

engine = create_engine(os.environ["DATABASE_URI"], convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

db_session = Session(engine)


metadata = MetaData()
tables = to_map("tomap")
# Todo: table with name "RssCurrentEtalons" is having a mapping problem temporally removed from a list

metadata.reflect(engine, only=tables)

Base = automap_base(metadata=metadata)
Base.query = session.query_property()
Base.prepare()
