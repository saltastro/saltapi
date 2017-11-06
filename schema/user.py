from data.user import *
from flask import g
from graphene_sqlalchemy import SQLAlchemyObjectType
import pandas as pd
from data.common import conn
import jwt
import  graphene
from graphene import ObjectType, String, List, Boolean, relay



class User:
    user_id = None
    user_setting = None
    user_value = None

    def __init__(self, user_id, setting, value):
        self.user_id = user_id
        self.user_setting = setting
        self.user_value = value

    @staticmethod
    def get_user_token(credentials):
        if credentials is None:
            return User._user_error(not_provided=True)
        try:

            username = credentials['credentials']['username']
            password = credentials['credentials']['password']
        except KeyError:
            return User._user_error(not_provided=True)

        user_id = User.query_id(username, password)

        if user_id is None:
            return User._user_error(not_found=True)
        return User.create_token(user_id)

    @staticmethod
    def basic_login(username, password):
        user_id = User.query_id(username, password)
        if user_id is None:
            return False
        User.current_user(user_id)
        return True

    @staticmethod
    def _user_error(not_provided=False, not_found=False):
        if not_provided:
            return {'errors': {'global': 'username or password not provide'}}

        if not_found:
            return {'errors': {'global': 'user not found'}}

    @staticmethod
    def query_id(username, password):
        """
        :param username: username
        :param password: password
        :return: PiptUser_Id or no if not found
        """
        sql = "SELECT PiptUser_Id From PiptUser where Username='{username}' AND Password=MD5('{password}')"\
            .format(username=username, password=password)
        result = pd.read_sql(sql, conn)

        try:
            return result.iloc[0]['PiptUser_Id']
        except IndexError:
            return None

    @staticmethod
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

    @staticmethod
    def is_valid_token(token):
        print(token)
        try:
            user = jwt.decode(token, "SECRET-KEY", algorithm='HS256')

            if 'user_id' in user:
                User.current_user(user['user_id'])
                return True
            return False
        except:
            return False

    @staticmethod
    def user_if_from_token(token):
        try:
            user = jwt.decode(token, "SECRET-KEY", algorithm='HS256')

            if 'user_id' in user:
                User.current_user(user['user_id'])
                return True
            return False
        except:
            return False

    @staticmethod
    def current_user(user_id):
        if user_id is not None:
            sql = "SELECT PiptUser_Id, PiptSetting_Id, Value FROM PiptUserSetting WHERE PiptSetting_Id = 20 " \
                  "  AND PiptUser_Id = {user_id}".format(user_id=user_id)
            result = pd.read_sql(sql, conn)
            g.user = User(result.iloc[0]['PiptUser_Id'], result.iloc[0]['PiptSetting_Id'], result.iloc[0]['Value'], )


class PiptUser(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptUserModel
        only_fields = ('PiptUser_Id', 'Username', 'Investigator')
    user_id = PiptUserModel.PiptUser_Id
    username = PiptUserModel.Username
    is_tac_chair = Boolean()
    partner_code = PartnerModel.Partner_Code
    partner_name = PartnerModel.Partner_Name

    def resolve_is_tac_chair(self, args, context, info):
        query = PiptUserTAC.get_query(info)
        result = query.filter(PiptUserTACModel.PiptUser_Id == self.user_id).first()
        return PiptUserTACModel.Chair


class PiptSetting(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptSettingModel


class PiptUserSetting(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptUserSettingModel


class PiptUserTAC(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptUserTACModel





user_list = [
    PiptUser,
    PiptSetting,
    PiptUserSetting,
    PiptUserTAC
]