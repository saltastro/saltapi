from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from tests.test_database import metadata, session


class User(object):
    query = session.query_property()

users = Table('PiptUser', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(50), unique=True),
              Column('email', String(120), unique=True)
)

mapper(User, users)
