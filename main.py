import pandas as pd

from data.common import conn
from app import jwt


class User:
    pipt_user_id = None
    username = None
    pipt_setting_ids = None
    values = None
    chair = None
    partner_id = None

    def __init__(self, user_cred):
        settings = []
        vas = []
        sql = "SELECT PiptUser.PiptUser_Id as PiptUser_Id, Username, Password, FirstName, Surname, PiptSetting_Id, Value, " \
              " Partner_Code, Chair" \
              "     FROM PiptUser " \
              "         JOIN Investigator using(Investigator_Id) " \
              "         JOIN PiptUserSetting on (PiptUser.PiptUser_Id = PiptUserSetting.PiptUser_Id) " \
              "         LEFT JOIN PiptUserTAC on (PiptUser.PiptUser_Id = PiptUserTAC.PiptUser_Id) " \
              "         LEFT JOIN Partner ON (PiptUserTAC.Partner_Id=Partner.Partner_Id)" \
              "     WHERE PiptUser.Username = '{username}' AND PiptUser.Password = md5('{password}') "\
            .format(username=user_cred["username"], password=user_cred["password"])

        user = pd.read_sql(sql, conn)
        if len(user['Username'].values[0]) > 0:
            # TODO: Handle permissions
            # for i, u in user.iterrows():
            #     settings.append(int(u['PiptSetting_Id']))
            #     vas.append(int(u['Value']))
            self.pipt_user_id = int(user["PiptUser_Id"].values[0])
            self.username = user['Username'].values[0]
            self.first_name = user['FirstName'].values[0]
            self.surname = user['Surname'].values[0]
            self.partner_code = user['Partner_Code'].values[0]
            # self.pipt_setting_ids = settings
            # self.values = vas
            self.chair = bool(int(user['Chair'].values[0])) if user['Chair'].values[0] is not None else False
        print(self.username)

    def get_token(self):
        """

        :param args:
        :return:
        """
        token_username = {"error": "user not valid"}
        """
        it creates a token for  the user using users username and password
        :param args: the users credentials(username and password)
        :return: user token
        """

        token_username = {'username': self.username}
        token = jwt.dumps(token_username)
        return token
