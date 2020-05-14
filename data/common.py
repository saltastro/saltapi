import pandas as pd
from flask import g
from data import sdb_connect
from util.action import Action


def find_proposals_allocated_time(partner_codes, semester):
    allocated_time_sql = """
SELECT DISTINCT ProposalCode_Id, Proposal_Code
FROM MultiPartner
    JOIN PriorityAlloc USING (MultiPartner_Id)
    JOIN Semester USING (Semester_Id)
    JOIN Partner USING (Partner_Id)
    JOIN ProposalCode USING (ProposalCode_Id)
WHERE Year = {year} AND Semester = {semester} AND Partner_Code IN ("{partner_codes}")
    """.format(
        semester=semester.split("-")[1],
        year=semester.split("-")[0],
        partner_codes='", "'.join(partner_codes)
    )
    conn = sdb_connect()
    results = pd.read_sql(allocated_time_sql, conn)
    conn.close()
    return results


def find_proposals_submitted(partner_codes, semester):
    submitted_sql = """
SELECT DISTINCT ProposalCode_Id, Proposal_Code
FROM Proposal
    JOIN ProposalCode USING(ProposalCode_Id)
    JOIN ProposalGeneralInfo USING (ProposalCode_Id)
    JOIN ProposalStatus USING (ProposalStatus_Id)
    JOIN Semester USING (Semester_Id)
    JOIN MultiPartner USING(ProposalCode_Id)
    JOIN Partner ON (MultiPartner.Partner_Id = Partner.Partner_Id)
WHERE Current = 1 AND Status NOT IN ("Deleted", "Rejected")
    AND Year = {year} AND Semester = {semester}
    AND Partner_Code IN ("{partner_codes}")
    """.format(
        semester=semester.split("-")[1],
        year=semester.split("-")[0],
        partner_codes='", "'.join(partner_codes)
    )
    conn = sdb_connect()
    results = pd.read_sql(submitted_sql, conn)
    conn.close()

    return results


def get_proposal_ids(semester, partner_code=None):

    conn = sdb_connect()
    all_partners = [p['Partner_Code'] for i, p in pd.read_sql("SELECT Partner_Code FROM Partner", conn).iterrows()]
    conn.close()

    user_partners = [partner for partner in all_partners if g.user.may_perform(Action.VIEW_PARTNER_PROPOSALS,
                                                                               partner=partner)]
    partner_codes = user_partners if partner_code is None else [partner_code]

    proposals_allocated_time = find_proposals_allocated_time(partner_codes=partner_codes, semester=semester)
    user_proposals = find_proposals_submitted(partner_codes=partner_codes, semester=semester)

    all_proposals = pd.concat([proposals_allocated_time, user_proposals], ignore_index=True).drop_duplicates()

    all_user_proposals = []
    for index, row in all_proposals.iterrows():
        if g.user.may_perform(Action.VIEW_PROPOSAL, proposal_code=str(row['Proposal_Code'])):
            all_user_proposals.append(str(row["ProposalCode_Id"]))
    return {
        'ProposalCode_Ids': all_user_proposals,
        "all_proposals": all_user_proposals,
    }


def proposal_code_ids_for_statistics(semester, partner_code=None):
    """
     Parameters
    ----------
    semester: str
        The Semester like "2019-2"
    partner_code: str
        The partner code like "RSA", "DC",...
     Returns
    -------
    iterable: str
        Array of proposal code ids
    """

    # TODO: find a better way to handle active partners
    # conn = sdb_connect()
    # all_partners = [p['Partner_Code'] for i, p in pd.read_sql("""
    # SELECT Partner_Code FROM Partner
    #     JOIN PartnerShareTimeDist USING(Partner_Id)
    #     JOIN Semester USING(Semester_Id)
    # WHERE `Virtual` = 0
    #     AND Semester_Id = {semester_id}
    #     AND TimePercent > 0
    # """.format(semester_id=query_semester_id(semester)), conn).iterrows()]
    # conn.close()
    all_partners = ['UW', 'RSA', 'UNC', 'UKSC', 'DC', 'RU', 'POL', 'AMNH', 'IUCAA', "GU", "DUR", "UC"]

    sql = """
SELECT distinct
    Partner.Partner_Code AS PartnerCode,
    ProposalCode_Id,
    Proposal_Code,
    ProposalStatus_Id ,
    CONCAT(Year, '-', Semester) AS Semester
FROM ProposalCode
    JOIN ProposalGeneralInfo USING(ProposalCode_Id)
    JOIN MultiPartner USING(ProposalCode_Id)
    JOIN ProposalContact USING(ProposalCode_Id)
    JOIN Investigator ON (Leader_Id=Investigator_Id)
    JOIN Semester USING(Semester_Id)
    JOIN Partner ON (MultiPartner.Partner_Id = Partner.Partner_Id)
GROUP BY ProposalCode_Id, Semester_Id HAVING Semester = "{semester}"
    AND ProposalStatus_Id NOT IN (9, 3)
    """.format(semester=semester)  # status 9 => Deleted, 3 => Rejected

    conn = sdb_connect()

    if partner_code is not None:
        sql += """  AND PartnerCode = "{partner_code}"
                    """.format(partner_code=partner_code)
    else:
        sql += """  AND PartnerCode IN ("{partner_codes}")
            """.format(partner_codes='", "'.join(all_partners))

    proposal_code_ids = []
    for index, r in pd.read_sql(sql, conn).iterrows():
        proposal_code_ids.append(str(r['ProposalCode_Id']))
    conn.close()
    return proposal_code_ids


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
