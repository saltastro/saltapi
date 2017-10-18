import pymysql
import os
from flask import g

sql_config = {
    'user': os.environ["SANDBOX_USER"],
    'host': os.environ["SANDBOX_HOST"],
    'passwd': os.getenv("SANDBOX_PASSWORD"),
    'db': os.getenv("SANDBOX_DATABASE"),
    'charset': 'utf8'
}

try:
    if g.TESTING:
        conn = pymysql.connect(**sql_config)
    else:
        conn = pymysql.connect(**sql_config)

except RuntimeError:
    conn = pymysql.connect(**sql_config)
