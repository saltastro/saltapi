from pymysql import connect
import os

sql_config = {
    'user': os.environ["API_USER"],
    'host': os.environ["API_HOST"],
    'passwd': os.getenv("API_PASSWORD"),
    'db': os.getenv("API_DATABASE"),
    'charset': 'utf8'
}


def sdb_connect():
    return connect(**sql_config)
