from flask import g
from util.action import Action
from data.common import sdb_connect
from util.error import InvalidUsage


def update_liaison_astronomers(assignments):
    """
    Update the database with a list of time allocations.

    Parameters
    ----------
    assignments : iterable
        The list of liaison astronomer assignments. Each assignment must be dictionary with a proposal code and
        a username (of the SALT Astronomer to be assigned to that proposal).
    """

    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for assignment in assignments:
                update_liaison_astronomer(proposal_code=assignment['proposalCode'],
                                          liaison_astronomer=assignment['liaisonAstronomer'],
                                          cursor=cursor)
            connection.commit()
    finally:
        connection.close()


def update_liaison_astronomer(proposal_code, liaison_astronomer, cursor):
    """
    Update a proposal's liaison astronomer.

    Parameters
    ----------
    proposal_code : str
        Proposal code of the proposal.
    liaison_astronomer : str
        Username of the liaison astronomer.
    cursor : database cursor
        Cursor on which the database command is executed.

    Returns
    -------
    void
    """

    if not g.user.may_perform(Action.UPDATE_LIAISON_ASTRONOMER,
                              proposal_code=proposal_code,
                              liaison_astronomer=liaison_astronomer):
        raise InvalidUsage(message='You are not allowed to update the liaison astronomer of proposal {proposal_code}'
                           .format(proposal_code=proposal_code),
                           status_code=403)

    if liaison_astronomer is not None:
        sql = '''UPDATE ProposalContact SET Astronomer_Id=
                        (SELECT PiptUser.Investigator_Id
                                FROM PiptUser
                         WHERE PiptUser.Username=%s)
                 WHERE ProposalContact.ProposalCode_Id=
                       (SELECT ProposalCode.ProposalCode_Id
                        FROM ProposalCode
                        WHERE ProposalCode.Proposal_Code=%s)'''
        params = (liaison_astronomer, proposal_code)
    else:
        sql = '''UPDATE ProposalContact SET Astronomer_Id=NULL
                 WHERE ProposalContact.ProposalCode_Id=
                       (SELECT ProposalCode.ProposalCode_Id
                        FROM ProposalCode
                        WHERE ProposalCode.Proposal_Code=%s)'''
        params = (proposal_code,)
    cursor.execute(sql, params)


def update_reviews(semester, reviews):
    """
    Update the database with a list of reviwes.

    Parameters
    ----------
    semester : str
        Semester, such as "2018-1".
    reviews : iterable
        The list of reviwews. Each assignment must be dictionary with a proposal code,
        a username (of the SALT Astronomer to be assigned as reviewer to that proposal)
        and a technical report (which may be None).
    """

    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for review in reviews:
                update_review(proposal_code=review['proposalCode'],
                              semester=semester,
                              reviewer=review['reviewer'],
                              report=review['report'],
                              cursor=cursor)
            connection.commit()
    finally:
        connection.close()


def update_review(proposal_code, semester, reviewer, report, cursor):
    """
    Update a proposal's reviewer.

    Parameters
    ----------
    proposal_code : str
        Proposal code of the proposal.
    semester : str
        Semester, such as "2018-1".
    reviewer : str
        Username of the reviewer.
    report : str
        Technical report.
    cursor : database cursor
        Cursor on which the database command is executed.

    Returns
    -------
    void
    """

    if not g.user.may_perform(Action.UPDATE_TECHNICAL_REVIEWS,
                              proposal_code=proposal_code,
                              reviewer=reviewer,
                              report=report):
        raise InvalidUsage(message='You are not allowed to make the requested review update for proposal {proposal_code}'
                           .format(proposal_code=proposal_code),
                           status_code=403)

    if not reviewer:
        raise InvalidUsage(message='A reviewer must be specified for a review',
                           status_code=403)

    year, sem = semester.split('-')
    sql = '''INSERT INTO ProposalTechReport (ProposalCode_Id, Semester_Id, Astronomer_Id, TechReport)
                    SELECT pc.ProposalCode_Id, s.Semester_Id, u.Investigator_Id, %s
                    FROM ProposalCode AS pc, Semester AS s, PiptUser AS u
                       WHERE pc.Proposal_Code=%s AND (s.Year=%s AND s.Semester=%s) AND  u.Username=%s
                ON DUPLICATE KEY UPDATE
                    ProposalCode_Id=
                        (SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code=%s),
                    Semester_Id=
                        (SELECT Semester_Id FROM Semester WHERE Year=%s AND Semester=%s),
                    Astronomer_Id=
                        (SELECT Investigator_Id FROM PiptUser WHERE Username=%s),
                    TechReport=%s'''
    params = (report, proposal_code, year, sem, reviewer, proposal_code, year, sem, reviewer, report)
    cursor.execute(sql, params)
