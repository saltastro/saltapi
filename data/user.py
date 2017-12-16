from flask import g
import pandas as pd
from data.common import sdb_connect
from schema.user import UserModel, Role
from data.partner import get_partners_for_role


def get_role(row, user_id):
    all_partner = get_partners_for_role()
    sql = "SELECT * " \
          "     FROM PiptUserSetting  " \
          "         LEFT JOIN PiptUserTAC using (PiptUser_Id) " \
          "     WHERE PiptSetting_Id = 22 " \
          "         AND PiptUser_Id = {user_id}".format(user_id=user_id)
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()

    role = []
    if not pd.isnull(row["Astro"]):
        role.append(
            Role(
                type="SALT_ASTRONOMER",
                partners=all_partner
            )
        )
    if not pd.isnull(row["Tac"]):
        partner = get_partners_for_role(ids=[row["TacPartner"]])
        role.append(
            Role(
                type="TAC_MEMBER",
                partners=partner
            )
        )

    if not pd.isnull(row["Chair"]) and row["Chair"] == 1:
        partner = get_partners_for_role(ids=[row["TacPartner"]])
        role.append(
            Role(
                type="TAC_CHAIR",
                partners=partner
            )
        )
    if len(results) > 0:

        role.append(
            Role(
                type="ADMINISTRATOR",
                partners=all_partner
            )
        )

    return role


def get_user(user_id):
    user = {}

    sql = " select *, t.PiptUser_Id as Tac, t.Partner_Id as TacPartner, a.Investigator_Id as Astro " \
          " from PiptUser as u " \
          " JOIN Investigator as i using (Investigator_Id) " \
          " left join SaltAstronomers as a using( Investigator_Id ) " \
          " left join PiptUserTAC as t on (u.PiptUser_Id = t.PiptUser_Id) " \
          " where u.PiptUser_Id = {user_id}".format(user_id=user_id)
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    username = ''
    for index, row in results.iterrows():
        username = row["Username"]
        if username not in user:
            user[username] = UserModel(
                username=row["Username"],
                first_name=row["FirstName"],
                last_name=row["Surname"],
                email=row["Email"],
                role=[]
            )
        user[username].role += get_role(row, user_id)
    return user[username]
