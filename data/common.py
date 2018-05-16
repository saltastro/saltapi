import pandas as pd
from flask import g
from data import sdb_connect
from util.action import Action


def get_proposal_ids(semester, partner_code=None):

    conn = sdb_connect()
    all_partners = [p['Partner_Code'] for i, p in pd.read_sql("SELECT Partner_Code FROM Partner", conn).iterrows()]
    conn.close()

    sql = """
SELECT distinct
    Partner.Partner_Code AS PartnerCode,
    ProposalCode_Id,
    Proposal_Code,
    Surname,
    ProposalStatus_Id ,
    CONCAT(Year, '-', Semester) AS Semester
FROM ProposalCode
    JOIN ProposalGeneralInfo USING(ProposalCode_Id)
    JOIN MultiPartner USING(ProposalCode_Id)
    JOIN ProposalContact USING(ProposalCode_Id)
    JOIN Investigator ON (Leader_Id=Investigator_Id)
    JOIN Semester USING(Semester_Id)
    OIN Partner ON (MultiPartner.Partner_Id = Partner.Partner_Id)
GROUP BY ProposalCode_Id, Semester_Id HAVING Semester = "{semester}"
    AND ProposalStatus_Id NOT IN (9, 3)
""".format(semester=semester)  # status 9 => Deleted, 3 => Rejected

    conn = sdb_connect()
    all_proposals = [str(p["ProposalCode_Id"]) for i, p in pd.read_sql(sql, conn).iterrows()]

    user_partners = [partner for partner in all_partners if g.user.may_perform(Action.VIEW_PARTNER_PROPOSALS,
                                                                               partner=partner)]
    if partner_code is not None:
        sql += """  AND PartnerCode IN ("{partner_codes}")
                """.format(partner_codes='", "'.join([partner_code]))
    else:
        sql += """  AND PartnerCode IN ("{partner_codes}")
        """.format(partner_codes='", "'.join(user_partners))

    proposal_code_ids = []
    for index, r in pd.read_sql(sql, conn).iterrows():
        if g.user.may_perform(Action.VIEW_PROPOSAL, proposal_code=str(r['Proposal_Code'])):
            proposal_code_ids.append(str(r['ProposalCode_Id']))
    conn.close()
    return {
        'ProposalCode_Ids': proposal_code_ids,
        "all_proposals": all_proposals
    }


def sql_list_string(values):
    """
    Generate a string for a list to use with the MySQL IN operator.

    For a non-empty list the list items are returned, separated by comma and surrounded by parentheses.
    For an empty list the string "(NULL)" is returned.

    Parameters
    ----------
    values : iterable of str
        List values

    Returns
    -------
    liststring : str
        String to use with MySQL's IN operator.

    """
    if values:
        return '({values})'.format(values=', '.join(values))
    return '(NULL)'
