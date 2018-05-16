import os

import pandas as pd

from data import sdb_connect
from data.common import get_proposal_ids, sql_list_string
from data.instruments import get_instruments
from data.proposal_data.allocations import proposals_allocated_time
from data.proposal_data.requested import get_proposals_requested_time, get_requested_per_partner
from data.proposal_data.technical_report import get_technical_reports
from data.proposal_data.text import get_proposals_text
from data.targets import get_targets
from util.semester import previous_semester

proposal_data = {}


def proposal_query(semester, proposal_code_ids, public):
    return """
    SELECT *
    FROM ProposalGeneralInfo
        JOIN ProposalStatus USING(ProposalStatus_Id)
        JOIN ProposalCode USING(ProposalCode_Id)
        LEFT JOIN P1Thesis USING(ProposalCode_Id)
        JOIN ProposalContact AS pc USING(ProposalCode_Id)
        JOIN P1ObservingConditions  USING(ProposalCode_Id)
        JOIN Transparency USING(Transparency_Id)
        JOIN Semester USING(Semester_Id)
    where CONCAT(Year, '-', Semester) = '{semester}' AND ProposalCode_Id IN {proposal_code_ids} ORDER BY ProposalCode_Id
    """.format(semester=semester, proposal_code_ids=proposal_code_ids) if public \
        else """
    SELECT *,
    i.FirstName as PIFirstName, i.Surname AS PILastName, i.Email AS PIEmail,
    c.FirstName AS PCFirstName, c.Surname AS PCLastName, c.Email AS PCEmail,
    tsa.FirstName AS SAFirstName, tsa.Surname AS SALastName, tsa.Email AS SAEmail,
    sau.Username AS SAUsername, piu.Username AS PIUsername, pcu.Username AS PCUsername
    FROM ProposalGeneralInfo
        JOIN ProposalStatus USING(ProposalStatus_Id)
        JOIN ProposalCode USING(ProposalCode_Id)
        LEFT JOIN P1Thesis USING(ProposalCode_Id)
        JOIN ProposalContact AS pc USING (ProposalCode_Id)
        JOIN Investigator AS i ON (i.Investigator_Id = pc.Leader_Id)
        JOIN Investigator AS c ON (c.Investigator_Id = pc.Contact_Id)
        LEFT JOIN Investigator AS tsa ON (tsa.Investigator_Id = pc.Astronomer_Id)
        LEFT JOIN PiptUser AS sau ON (sau.Investigator_Id = pc.Astronomer_Id)
        LEFT JOIN PiptUser AS piu ON (piu.Investigator_Id = pc.Leader_Id)
        LEFT JOIN PiptUser AS pcu ON (pcu.Investigator_Id = pc.Contact_Id)
        JOIN P1ObservingConditions USING(ProposalCode_Id)
        JOIN Transparency USING(Transparency_Id)
        JOIN Semester USING(Semester_Id)
    where CONCAT(Year, '-', Semester) = '{semester}' AND ProposalCode_Id IN {proposal_code_ids} ORDER BY ProposalCode_Id
    """.format(semester=semester, proposal_code_ids=proposal_code_ids)


def make_proposal(row, public):
    from schema.proposal import Proposal, User

    sa = User(
        first_name=row["SAFirstName"],
        last_name=row["SALastName"],
        email=row["SAEmail"],
        username=row["SAUsername"]
    ) if row["SAFirstName"] is not None else User()
    return Proposal(
        allocated_time=[],
        code=row["Proposal_Code"],
        instruments=[],
        is_target_of_opportunity=row["ActOnAlert"] == 1,
        is_thesis=not pd.isnull(row["ThesisType_Id"]),
        is_p4=row["P4"] == 1,
        liaison_salt_astronomer=User() if public else sa,
        max_seeing=row["MaxSeeing"],
        principal_contact=User() if public else User(
            first_name=row["PCFirstName"],
            username=row["PCUsername"],
            last_name=row["PCLastName"],
            email=row["PCEmail"]
        ),
        principal_investigator=User() if public else User(
            first_name=row["PIFirstName"],
            username=row["PIUsername"],
            last_name=row["PILastName"],
            email=row["PIEmail"]
        ),
        status=row["Status"],
        tac_comment=[],
        targets=[],
        tech_reviews=[],
        time_requests=[],
        transparency=row["Transparency"]
    )


def fill_proposal_private_data(proposals, text, reviews, requests):
    from schema.proposal import User, TechReview
    for code in list(proposals.keys()):
        proposals[code].title = text[code]['title']
        proposals[code].abstract = text[code]['abstract']
        proposals[code].time_requests = requests[code]
        try:
            for tre in reviews[code]:

                reviewer = User(
                    first_name=tre["ReviewerFirstName"],
                    last_name=tre["ReviewerLastName"],
                    email=tre["ReviewerEmail"],
                    username=tre["ReviewerUsername"]
                ) if tre['ReviewerFirstName'] is not None else User()
                proposals[code].tech_reviews.append(
                    TechReview(semester=tre['Semester'], reviewer=reviewer, report=tre['Report'])
                )
        except:
            pass


def query_proposal_data(proposal_code_ids, semester, public=False):

    proposals = {}
    proposals_text = get_proposals_text(proposal_code_ids)
    tech_reports = get_technical_reports(proposal_code_ids)
    requested_times = get_proposals_requested_time(proposal_code_ids)

    proposal_sql = proposal_query(semester, proposal_code_ids, public=public)

    conn = sdb_connect()
    results = pd.read_sql(proposal_sql, conn)
    for index, row in results.iterrows():
        if row["Proposal_Code"] not in proposals:
            proposals[row["Proposal_Code"]] = make_proposal(row, public)

    get_instruments(proposal_code_ids, proposals)
    get_targets(proposal_code_ids=proposal_code_ids, proposals=proposals)
    fill_proposal_private_data(proposals, proposals_text, tech_reports, requested_times)

    get_requested_per_partner(proposal_code_ids, proposals)

    proposals_allocated_time(semester, proposals)
    return proposals.values()


def get_proposals(**args):
    semester = args['semester']
    partner = args['partner_code']
    public = args['details']
    ids = get_proposal_ids(semester, partner)
    proposal_code_ids = sql_list_string(ids['ProposalCode_Ids'])
    data = query_proposal_data(proposal_code_ids, semester, public=public)
    return data


def liaison_astronomer(proposal_code):
    """
    The liaison astronomer for a proposal. The astronomer's username is returned.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-007".

    Returns
    -------
    username : str
        The liaison astronomer's username.

    """
    sql = '''SELECT PiptUser.Username AS LiaisonAstronomer
       FROM PiptUser
       RIGHT JOIN Investigator USING (PiptUser_Id)
       RIGHT JOIN ProposalContact ON Investigator.Investigator_Id = ProposalContact.Astronomer_Id
       RIGHT JOIN ProposalCode USING (ProposalCode_Id)
       WHERE ProposalCode.Proposal_Code=%s'''
    df = pd.read_sql(sql, params=(proposal_code,), con=sdb_connect())

    return df['LiaisonAstronomer'][0]


def technical_reviewer(proposal_code):
    """
    The reviewer for a proposal. The reviewer's username is returned.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-007".

    Returns
    -------
    username : str
        The reviewer's username.

    """
    sql = '''SELECT PiptUser.Username AS Reviewer
       FROM PiptUser
       RIGHT JOIN Investigator USING (PiptUser_Id)
       RIGHT JOIN ProposalTechReport ON Investigator.Investigator_Id = ProposalTechReport.Astronomer_Id
       RIGHT JOIN ProposalCode USING (ProposalCode_Id)
       WHERE ProposalCode.Proposal_Code=%s'''
    df = pd.read_sql(sql, params=(proposal_code,), con=sdb_connect())

    return df['Reviewer'][0]


def is_investigator(username, proposal_code):
    """
    Check whether a user is investigator on a proposal.

    Parameters
    ----------
    username : str
        The username.
    proposal_code : str
        The proposal code, such as "2018-1-SCI-007".

    Returns
    -------
    isinvestigator : bool
        Whether the user is an investigator on the proposal.
    """

    sql = '''
SELECT COUNT(*) AS Count
       FROM ProposalContact AS ProposalContact
       JOIN ProposalCode ON ProposalContact.ProposalCode_Id = ProposalCode.ProposalCode_Id
       JOIN Investigator ON ProposalContact.Astronomer_Id = Investigator.Investigator_Id
       JOIN PiptUser ON Investigator.PiptUser_Id = PiptUser.PiptUser_Id
WHERE ProposalCode.Proposal_Code = %s AND PiptUser.Username = %s
'''
    conn = sdb_connect()
    df = pd.read_sql(sql, conn, params=(proposal_code, username))
    conn.close()

    return df['Count'][0] > 0


def latest_version(proposal_code, phase):
    """
    The latest version number of a proposal, given a proposal phase.

    This function requires the environment variable PROPOSALS_DIR to exist. Its value must be the absolute file path
    to the directory containing all the proposal content.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-009".
    phase : int
        The proposal phase (1 or 2).

    Returns
    -------
    version : number
        The current version number.
    """

    sql = '''
SELECT Proposal.Submission AS Submission
       FROM Proposal
       JOIN ProposalCode ON Proposal.ProposalCode_Id = ProposalCode.ProposalCode_Id
WHERE ProposalCode.Proposal_Code = %s AND Proposal.Phase = %s
ORDER BY Proposal.Submission DESC
LIMIT 1
'''
    conn = sdb_connect()
    df = pd.read_sql(sql, conn, params=(proposal_code, phase))
    conn.close()

    if not len(df['Submission']):
        raise Exception('Proposal {proposal_code} does not have any submitted version for phase {phase}'
                        .format(proposal_code=proposal_code, phase=phase))

    return df['Submission'][0]


def summary_file(proposal_code, semester):
    """
    The file path of a proposal's summary file. The summary file is the progress report (if there is
    one) or the phase 1 summary. If there exists a supplementary file for the progress report, a
    temporary file containing both the progress report and the supplementary file is created, and
    the path to that temporary file is returned.

    The semester is the one for whose time allocation the summary should be used. This is relevant
    only for progress reports. Note that the progress report is returned for the semester previous to
    the given one. So, for example, if '2018-1' is passed as semester, the progress report for 2017-2
    is returned.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-005".
    semester : str
        The semester, such as '2018-1'.

    Returns
    -------
    filepath : str
        The file path of the summary.
    """

    # look for a progress report and a supplementary file
    prev_sem = previous_semester(semester)
    sql = '''
SELECT ProposalProgress.ReportPath AS ReportPath
       FROM ProposalProgress
       JOIN ProposalCode USING (ProposalCode_Id)
       JOIN Semester USING (Semester_Id)
WHERE ProposalCode.Proposal_Code = %s AND CONCAT(Semester.Year, '-', Semester.Semester) = %s
'''

    conn = sdb_connect()
    df = pd.read_sql(sql, conn, params=(proposal_code, prev_sem))
    conn.close()

    if len(df['ReportPath']) > 0:
        report = os.path.join(os.environ['PROPOSALS_DIR'],
                              proposal_code,
                              'Included',
                              df['ReportPath'][0])
        return report
    else:
        summary = os.path.join(os.environ['PROPOSALS_DIR'],
                               proposal_code,
                               str(latest_version(proposal_code, 1)),
                               'Summary.pdf')
        return summary
