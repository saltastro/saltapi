from logging import log
from pymysql import connect
import os
from flask import abort

sql_config = {
    'user': os.environ["API_USER"],
    'host': os.environ["API_HOST"],
    'passwd': os.getenv("API_PASSWORD"),
    'db': os.getenv("API_DATABASE"),
    'charset': 'utf8'
}


def sdb_connect():
    try:
        return connect(**sql_config)
    except Exception as err:
        raise RuntimeError("Failed to connect to sdb")
        # TODO: Log exception

