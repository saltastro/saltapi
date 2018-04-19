from flask import g
import pandas as pd
from data.common import sdb_connect
from schema.user import UserModel, Role, RoleType, TacMember
from data.partner import get_partners_for_role
from util.action import Action
from util.error import InvalidUsage


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
                type=RoleType.SALT_ASTRONOMER,
                partners=all_partner
            )
        )
    if not pd.isnull(row["Tac"]):
        partner = get_partners_for_role(ids=[row["TacPartner"]])
        role.append(
            Role(
                type=RoleType.TAC_MEMBER,
                partners=partner
            )
        )

    if not pd.isnull(row["Chair"]) and row["Chair"] == 1:
        partner = get_partners_for_role(ids=[row["TacPartner"]])
        role.append(
            Role(
                type=RoleType.TAC_CHAIR,
                partners=partner
            )
        )

    if len(results) > 0 and int(results.iloc[0]["Value"]) > 1:

        role.append(
            Role(
                type=RoleType.ADMINISTRATOR,
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


def get_salt_users():
    sql = 'select * from PiptUser JOIN Investigator using (Investigator_Id)'
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    users = []
    for index, row in results.iterrows():
        if row["Username"] is not None:
            users.append(UserModel(
                username=row["Username"],
                first_name=row["FirstName"],
                last_name=row["Surname"],
                email=row["Email"],
                role=[]
            ))

    return users

def get_tac_members(partner):
    sql = '''select * from PiptUser
join PiptUserTAC using(PiptUser_Id)
join Investigator using(Investigator_Id)
join Partner using(Partner_Id)
        '''
    if partner is not None:
        sql += " where Partner_Code = '{partner}'".format(partner=partner)
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    tacs = []
    for index, row in results.iterrows():
        if row["Username"] is not None:
            tacs.append(TacMember(
                username=row["Username"],
                first_name=row["FirstName"],
                last_name=row["Surname"],
                email=row["Email"],
                partner_code=row["Partner_Code"],
                partner_name=row["Partner_Name"],
                is_chair=row["Chair"] == 1
            ))

    return tacs


def update_tac_member(partner, member, cursor):
    """
    Update a proposal's reviewer.

    Parameters
    ----------
    partner : str
        partner updating member.
    member : str
        username of a member.
    cursor : database cursor
        Cursor on which the database command is executed.

    Returns
    -------
    void
    """

    if not g.user.may_perform(Action.UPDATE_TAC_COMMENTS,
                              partner=partner):
        raise InvalidUsage(message='You are not allowed to update members of {partner}'
                           .format(partner=partner),
                           status_code=403)


    sql = '''
    INSERT INTO PiptUserTAC (PiptUser_Id, Partner_Id, Chair)
SELECT PiptUser_Id, Partner_Id, 0
FROM PiptUser join Partner on (Partner_Code = %s)
WHERE  Username = %s
ON DUPLICATE KEY UPDATE
    PiptUser_Id=
        (SELECT PiptUser_Id FROM PiptUser WHERE  Username = %s),
    Partner_Id=
        (SELECT  Partner_Id FROM  Partner WHERE Partner_Code = %s),
    Chair=0'''
    params = (partner, member, member, partner)
    cursor.execute(sql, params)


def update_tac_members(partner, members):
    """
    Update the database with a list of members.

    Parameters
    ----------
    partner : str
       Partner code like "RSA".
    members : iterable
        The list of user names of members..
    """

    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for member in members:
                update_tac_member(
                    partner=partner,
                    member=member['member'],
                    cursor=cursor)
            connection.commit()
    finally:
        connection.close()
