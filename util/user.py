from flask import g
import pandas as pd
from data.common import sdb_connect
from data.user import get_user
import jwt

def get_user_token(credentials):
    if credentials is None:
        return _user_error(not_provided=True)
    try:

        username = credentials['credentials']['username']
        password = credentials['credentials']['password']
    except KeyError:
        return _user_error(not_provided=True)

    user_id = query_id(username, password)

    if user_id is None:
        return _user_error(not_found=True)
    return create_token(user_id)

def basic_login(username, password):
    user_id = query_id(username, password)
    if user_id is None:
        return False
    current_user(user_id)
    return True

def _user_error(not_provided=False, not_found=False):
    if not_provided:
        return {'errors': {'global': 'username or password not provide'}}

    if not_found:
        return {'errors': {'global': 'user not found'}}

def query_id(username, password):
    """
    :param username: username
    :param password: password
    :return: PiptUser_Id or no if not found
    """
    sql = "SELECT PiptUser_Id From PiptUser where Username='{username}' AND Password=MD5('{password}')" \
        .format(username=username, password=password)

    conn = sdb_connect()
    try:
        result = pd.read_sql(sql, conn)
        conn.close()
        return result.iloc[0]['PiptUser_Id']
    except IndexError:
        return None

def create_token(user_id):
    """
    Create a token containing the given user id.

    :param user_id:
    :return: the token
    """
    user = {
        'user_id': '{user_id}'.format(user_id=user_id)
    }
    token = jwt.encode(user, "SECRET-KEY", algorithm='HS256').decode('utf-8')

    return token

def is_valid_token(token):
    try:
        user = jwt.decode(token, "SECRET-KEY", algorithm='HS256')

        if 'user_id' in user:
            current_user(user['user_id'])
            return True
        return False
    except Exception as e:
        return False

def user_if_from_token(token):
    try:
        user = jwt.decode(token, "SECRET-KEY", algorithm='HS256')

        if 'user_id' in user:
            current_user(user['user_id'])
            return True
        return False
    except:
        return False

def current_user(user_id):
    if user_id is not None:
        g.user = get_user(user_id)
