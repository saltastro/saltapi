from collections import namedtuple
import pandas as pd

from data import sdb_connect

TimeRequest = namedtuple('TimeRequest', ('semester', 'partner', 'time_request'))


def time_requests(proposal_code):
    """
    A proposal's time requests for all semesters and partners.

    Parameters
    ----------
    proposal_code : str
        Proposal code, such as "2018-1-SCI-008".

    Returns
    -------
    timerequests : list of TimeRequest
        The time requests.
    """

    sql = '''
SELECT CONCAT(semester.Year, '-', semester.Semester) AS Semester,
       partner.Partner_Code AS Partner_Code,
       multipartner.ReqTimeAmount * multipartner.ReqTimePercent / 100 AS Time_Request
       FROM MultiPartner AS multipartner
       JOIN Semester AS semester ON multipartner.Semester_Id = semester.Semester_Id
       JOIN Partner AS partner ON multipartner.Partner_Id = partner.Partner_Id
       JOIN ProposalCode AS proposalcode ON multipartner.ProposalCode_Id = proposalcode.ProposalCode_Id
WHERE proposalcode.Proposal_Code=%s
'''
    conn = sdb_connect()
    df = pd.read_sql(sql, conn, params=(proposal_code,))
    conn.close()

    return [TimeRequest(semester=row[1]['Semester'],
                        partner=row[1]['Partner_Code'],
                        time_request=row[1]['Time_Request'])
            for row in df.iterrows()]
