from flask import g
import pandas as pd
from data.common import sdb_connect
from schema.partner import Partner
from schema.user import User, TacMember
from util.action import Action
from util.error import InvalidUsage


def get_user(user_id):
    user = {}

    sql = '''
SELECT
    Username, FirstName, Surname, Email
FROM PiptUser AS u
    JOIN Investigator AS i using (Investigator_Id)
WHERE u.PiptUser_Id = {user_id}
'''.format(user_id=user_id)
    conn = sdb_connect()
    user_details_results = pd.read_sql(sql, conn)
    conn.close()
    username = user_details_results.iloc[0]["Username"]
    if username not in user:
        user[username] = User(
            user_id=user_id,
            username=username,
            first_name=user_details_results.iloc[0]["FirstName"],
            last_name=user_details_results.iloc[0]["Surname"],
            email=user_details_results.iloc[0]["Email"],
            roles=[]
        )

    return user[username]


def get_salt_users():
    sql = 'SELECT * FROM PiptUser JOIN Investigator USING (Investigator_Id)'
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    users = []
    for index, row in results.iterrows():
        if row["Username"] is not None:
            users.append(User(
                username=row["Username"],
                first_name=row["FirstName"],
                last_name=row["Surname"],
                email=row["Email"],
                role=[]
            ))

    return users


def get_tac_members(partner):
    sql = '''
SELECT *
FROM PiptUser
    JOIN PiptUserTAC USING(PiptUser_Id)
    JOIN Investigator USING(Investigator_Id)
    JOIN Partner USING(Partner_Id)
'''
    if partner is not None:
        sql += " WHERE Partner_Code = '{partner}'".format(partner=partner)
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
                partner=Partner(
                    code=row["Partner_Code"],
                    name=row["Partner_Name"]
                ),
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
