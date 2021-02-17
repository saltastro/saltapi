from flask import g
from util.action import Action
from data.common import sdb_connect
from util.error import InvalidUsage


def update_completion_comments(semester, completion_comments):
    """
    Update the database with a list of reviwes.

    Parameters
    ----------
    semester : str
        Semester, such as "2018-1".
    completion_comments : iterable
        The list of completion_comments. Each assignment must be dictionary with a proposal code,
        and a completion comment (which may be None).
    """

    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for comment in completion_comments:
                update_completion_comment(
                    proposal_code=comment['proposalCode'],
                    semester=semester,
                    comment=comment['comment'],
                    cursor=cursor
                )
            connection.commit()
    finally:
        connection.close()


def update_completion_comment(proposal_code, semester, comment, cursor):
    """
    Update a proposal's reviewer.

    Parameters
    ----------
    proposal_code : str
        Proposal code of the proposal.
    semester : str
        Semester, such as "2018-1".
    comment : str
        Completion Stat comment.
    cursor : database cursor
        Cursor on which the database command is executed.

    Returns
    -------
    void
    """

    if not g.user.may_perform(Action.UPDATE_COMPLETION_STAT_COMMENT,
                              proposal_code=proposal_code,
                              comment=comment,
                              semester=semester):
        raise InvalidUsage(message='You are not allowed to make the requested update for proposal {proposal_code}'
                           .format(proposal_code=proposal_code),
                           status_code=403)

    year, sem = semester.split('-')

    sql = '''UPDATE ProposalText SET CompletionComment=%s WHERE 
              ProposalCode_Id=(SELECT ProposalCode_Id FROM ProposalCode WHERE Proposal_Code=%s) AND 
              Semester_Id=(SELECT Semester_Id FROM Semester WHERE Year=%s AND Semester=%s)'''
    params = (comment, proposal_code, year, sem)
    cursor.execute(sql, params)
