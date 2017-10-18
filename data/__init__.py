import pymysql
import os
from flask import g

sql_config = {
    'user': os.environ["API_USER"],
    'host': os.environ["API_HOST"],
    'passwd': os.getenv("API_PASSWORD"),
    'db': os.getenv("API_DATABASE"),
    'charset': 'utf8'
}

try:
    if g.TESTING:
        conn = pymysql.connect(**sql_config)
    else:
        conn = pymysql.connect(**sql_config)

except RuntimeError:
    conn = pymysql.connect(**sql_config)
