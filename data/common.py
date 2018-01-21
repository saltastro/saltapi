import pandas as pd
from flask import g
from data import sdb_connect
from util.action import Action


def get_proposal_ids(semester, partner_code=None):

    conn = sdb_connect()
    g.ALL_PARTNERS = [p['Partner_Code'] for i, p in pd.read_sql("SELECT Partner_Code FROM Partner", conn).iterrows()]
    conn.close()

    sql = """ 
            SELECT MAX(p.Proposal_Id) as Ids, pc.ProposalCode_Id as PCode_Ids, pc.Proposal_Code as PCD 
                FROM Proposal AS p 
                    JOIN ProposalCode AS pc ON (p.ProposalCode_Id=pc.ProposalCode_Id) 
                    JOIN MultiPartner AS mp ON (p.ProposalCode_Id=mp.ProposalCode_Id) 
                    JOIN Partner AS pa ON (mp.Partner_Id=pa.Partner_Id) 
                    JOIN Semester AS sm ON (mp.Semester_Id=sm.Semester_Id) 
                    JOIN ProposalGeneralInfo AS pgi ON (pgi.ProposalCode_Id=p.ProposalCode_Id) 
                    JOIN ProposalInvestigator AS pi ON (pi.ProposalCode_Id=p.ProposalCode_Id) 
                    JOIN Investigator as i ON (i.Investigator_Id = pi.Investigator_Id) 
                WHERE Phase=1 AND ProposalStatus_Id not in (4, 9, 6, 8, 5, 3, 100) 
                    AND CONCAT(sm.Year, '-', sm.Semester) = '{semester}' 
               """.format(semester=semester)
    all_sql = sql + " GROUP BY pc.ProposalCode_Id "
    conn = sdb_connect()
    all_proposals = [str(p["Ids"]) for i, p in pd.read_sql(all_sql, conn).iterrows()]


    partners = [partner for partner in g.ALL_PARTNERS if g.user.may_perform(Action.VIEW_PARTNER_PROPOSALS, partner)]

    sql += """ AND (
                    pa.Partner_Code in ("{partner_codes}")
                    OR
                    i.Email = \"{email}\"
                    ) 
            """.format(partner_codes='", "'.join(partners),
                       email=g.user.email)

    if partner_code is not None:
        sql += " AND pa.Partner_Code = '{partner_code}' ".format(partner_code=partner_code)

    ids = []
    pcode_ids = []
    for index, r in pd.read_sql(sql + " GROUP BY pc.ProposalCode_Id ", conn).iterrows():
        ids.append(str(r['Ids']))
        pcode_ids.append(str(r['PCode_Ids']))
    conn.close()
    return {'ProposalIds': ids, 'ProposalCode_Ids': pcode_ids, "all_proposals": all_proposals}
