import pandas as pd
from data import sdb_connect


def multipartner_ids(proposal_codes, partner, semester):
    """
    Map proposal codes to multipartner ids.

    Proposal codes are ignored if the proposal doesn't have a multipartner entry for the partner and semester.

    Parameters
    ----------
    proposal_codes : iterable
        The proposal codes to map.
    partner : str
        The partner code, such as `RSA` or `IUCAA`.
    semester : str
        The semester, such as `2017-2` or `2018-1`.

    Returns
    -------
    ids: dict
       A dictionary of proposal codes and multipartner ids.
    """

    year, sem = semester.split('-')
    proposal_code_strings = ["'{proposal_code}'".format(proposal_code=proposal_code)
                             for proposal_code in proposal_codes]
    sql = '''SELECT pc.Proposal_Code, mp.MultiPartner_Id
                    FROM MultiPartner AS mp
                    JOIN ProposalCode AS pc USING (ProposalCode_Id)
                    JOIN Partner AS p USING (Partner_Id)
                    JOIN Semester AS s USING (Semester_Id)
                    WHERE pc.Proposal_Code IN ({proposal_codes})
                          AND p.Partner_Code='{partner_code}'
                          AND (s.Year={year} AND s.Semester={semester})'''.format(
        proposal_codes=', '.join(proposal_code_strings),
        partner_code=partner,
        year=year,
        semester=sem)

    connection = sdb_connect()
    df = pd.read_sql(sql, connection)
    connection.close()

    return {item['Proposal_Code']: item['MultiPartner_Id'] for item in df.to_dict('records')}