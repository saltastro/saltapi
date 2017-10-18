import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import hashlib

Base = declarative_base()
engine = create_engine('sqlite:///test.db')

session = sessionmaker(bind=engine)
db_session = Session(engine)


def setup_db():
    pass


class User(Base):
    __tablename__ = 'PiptUser'
    PiptUser_Id = Column(Integer, primary_key=True)
    Username = Column(String(250), nullable=False)
    Password = Column(String(250), nullable=False)
    Investigator_Id = Column(String(250), nullable=False)
    EmailValidation = Column(String(250))
    Active = Column(Integer)
    ReceiveNews = Column(Integer)
    HideLargeContent = Column(Integer)


class InitData:
    @staticmethod
    def test_user():
        Base.metadata.bind = engine
        cursor = session()

        # none existing Test user
        def set_password(password):
            return hashlib.md5(password).hexdigest()
        test_user = User(
            Username="test_user",
            Password=set_password("test123"),
            Investigator_Id=-99,
            EmailValidation=None,
            Active=-99,
            ReceiveNews=-99,
            HideLargeContent=-99
        )
        cursor.add(test_user)
        cursor.commit()


Base.metadata.create_all(engine)
