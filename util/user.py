from flask import g
import os
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

    try:
        verify_user(username, password)
        return create_token(username)
    except Exception:
        return _user_error(not_found=True)


def basic_login(username, password):
    try:
        verify_user(username, password)
        user_id = query_id(username)
    except Exception:
        user_id = None
    if user_id is None:
        return False
    set_current_user(user_id)
    return True


def _user_error(not_provided=False, not_found=False):
    if not_provided:
        return {'errors': {'global': 'username or password not provide'}}

    if not_found:
        return {'errors': {'global': 'user not found'}}


def verify_user(username, password):
    """
    :param username: username
    :param password: password
    :return: PiptUser_Id or None if not found
    """
    sql = """SELECT COUNT(PiptUser_Id) AS UserCount
             FROM PiptUser
             WHERE Username='{username}' AND Password=MD5('{password}')""" \
        .format(username=username, password=password)

    conn = sdb_connect()
    result = pd.read_sql(sql, conn)
    conn.close()
    if not result.iloc[0]['UserCount']:
        raise Exception('Username or password wrong')


def query_id(username):
    """
    :param username: username
    :return: PiptUser_Id or None if not found
    """
    sql = """SELECT PiptUser_Id
             FROM PiptUser
             WHERE Username='{username}'""" \
        .format(username=username)

    conn = sdb_connect()
    try:
        result = pd.read_sql(sql, conn)
        conn.close()
        return result.iloc[0]['PiptUser_Id']
    except IndexError:
        return None


def create_token(username):
    """
    Create a token containing the given user id.

    :param username:
    :return: the token
    """

    user_id = query_id(username)
    if user_id is None:
        raise Exception('User not found')
    user = {
        'user_id': '{user_id}'.format(user_id=user_id)
    }
    token = jwt.encode(user, os.environ['SECRET_TOKEN_KEY'], algorithm='HS256').decode('utf-8')

    return token


def is_valid_token(token):
    try:
        user = jwt.decode(token, os.environ['SECRET_TOKEN_KEY'], algorithm='HS256')

        if 'user_id' in user:
            set_current_user(user['user_id'])
            return True
        return False
    except Exception as e:
        return False


def user_if_from_token(token):
    try:
        user = jwt.decode(token, os.environ['SECRET_TOKEN_KEY'], algorithm='HS256')

        if 'user_id' in user:
            set_current_user(user['user_id'])
            return True
        return False
    except:
        return False


def set_current_user(user_id):
    if user_id is not None:
        g.user = get_user(user_id)
