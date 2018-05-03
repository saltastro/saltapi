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


def update_tac_member(partner, member, is_chair, cursor):
    """
    Update or add a tac member to be TAC on given partner.

    Parameters
    ----------
    partner : str
        The partner code (such as "RSA") of the partner whose TAC is updated
    member : str
        The username of the added/updated TAC member.
    is_chair: boolean
        true if user is a chair
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
    chair = 1 if is_chair else 0
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
        Chair=%s'''
    params = (partner, member, member, partner, chair)
    cursor.execute(sql, params)


def remove_tac_member(partner, member, cursor):
    """
    Remove a member from a partner's TAC.

    Parameters
    ----------
    partner : str
       The partner code (such as "RSA") of the partner whose TAC is updated.
    member : str
        The username of the TAC member to be removed.
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
DELETE FROM PiptUserTAC
WHERE
    PiptUser_Id = (SELECT PiptUser_Id FROM PiptUser WHERE  Username = %s)
    AND
    Partner_Id = (SELECT  Partner_Id FROM  Partner WHERE Partner_Code = %s)
'''
    params = (member, partner)
    cursor.execute(sql, params)


def update_tac_members(partner, members):
    """
    Add or update a list of members for a partner's TAC.
    If a member is not in the database, they are added. Otherwise their details are updated in the database.

    Parameters
    ----------
    partner : str
       Partner code like "RSA".
    members : iterable
        The list of usernames of members, like
        like [
            {member: 'user-1', is_chair: False},
            {member: 'user-4', is_chair: True}
        ]
    """

    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for member in members:
                update_tac_member(
                    partner=partner,
                    member=member['member'],
                    is_chair=member['is_chair'],
                    cursor=cursor)
                connection.commit()

    finally:
        connection.close()


def remove_tac_members(partner, members):
    """
    Remove a list of members from a partner's TAC.

    Parameters
    ----------
    partner : str
        Partner code like "RSA".
    members : iterable
        The list of usernames of members, like [{member: 'user-1'}, {member: 'user-4'}]
    """

    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for member in members:
                remove_tac_member(
                    partner=partner,
                    member=member['member'],
                    cursor=cursor)
            connection.commit()
    finally:
        connection.close()
