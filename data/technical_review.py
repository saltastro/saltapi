from flask import g
from util.action import Action

def update_technical_report(proposal_code, semester, report, username, cursor):
    """
    Update the ProposalTechReport table.

    If no entry exists for the proposal and semester, a new entry is created with the given username
    as reporting astronomer. If an entry exists, its TechReport column value is updated, but the
    reporting user is left unchanged.

    This function executes the insert statement on the given cursor, but it does not explicitly
    commit. You might have to commit the transaction in a function using this one.

    Parameters
    ----------
    proposal_code : str
        Proposal code of the proposal.
    semester : str
        Semester, such as '2017-2; or '2018-1'.
    report : str
        Technical report.
    username : str
        Username of the reporting astronomer.
    cursor: database cursor
        Cursor on which the insert command is executed.

    Returns
    -------
       void

    """

    if not g.user.may_perform(Action.UPDATE_TECHNICAL_REPORT, proposal_code=proposal_code):
        raise Exception('You are not allowed to update the technical report of proposal {proposal_code}'
                        .format(proposal_code=proposal_code))

    year, sem = semester.split('-')
    sql = '''INSERT INTO ProposalTechReport (ProposalCode_Id, Semester_Id, Astronomer_Id, TechReport)
                    SELECT pc.ProposalCode_Id, s.Semester_Id, u.PiptUser_Id, %s
                           FROM ProposalCode AS pc, Semester AS s, PiptUser AS u
                           WHERE pc.Proposal_Code=%s AND (s.Year=%s AND s.Semester=%s) AND  u.Username=%s
                    ON DUPLICATE KEY UPDATE TechReport=%s'''
    cursor.execute(sql, (report, proposal_code, year, sem, username, report))


