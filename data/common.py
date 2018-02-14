import pandas as pd
from flask import g
from data import sdb_connect
from util.action import Action


def get_proposal_ids(semester, partner_code=None):

    conn = sdb_connect()
    all_partners = [p['Partner_Code'] for i, p in pd.read_sql("SELECT Partner_Code FROM Partner", conn).iterrows()]
    conn.close()

    sql = """
        select distinct Partner.Partner_Code as PartnerCode, ProposalCode_Id, Proposal_Code, Surname, ProposalStatus_Id , CONCAT(Year, '-', Semester) as Semester
            from ProposalCode
                join ProposalGeneralInfo using (ProposalCode_Id)
                join MultiPartner using (ProposalCode_Id)
                join ProposalContact using (ProposalCode_Id)
                join Investigator on (Leader_Id=Investigator_Id)
                join Semester using (Semester_Id)
                join Partner on (MultiPartner.Partner_Id = Partner.Partner_Id)
            Group by ProposalCode_Id, Semester_Id having Semester = "{semester}"
                and sum(ReqTimeAmount) > 0
                and ProposalStatus_Id NOT IN (9, 3)
                """.format(semester=semester)

    conn = sdb_connect()
    all_proposals = [str(p["ProposalCode_Id"]) for i, p in pd.read_sql(sql, conn).iterrows()]

    user_partners = [partner for partner in all_partners if g.user.may_perform(Action.VIEW_PARTNER_PROPOSALS,
                                                                               partner=partner)]
    if partner_code is not None:
        sql += """  and PartnerCode in ("{partner_codes}")
                """.format(partner_codes='", "'.join([partner_code]))
    else:
        sql += """  and PartnerCode in ("{partner_codes}")
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
