import pandas as pd
from logging import log
from data import sdb_connect
import datetime
import warnings
from dateutil.relativedelta import relativedelta


def get_proposal_ids(semester, partner_code=None, proposal_code=None, all_proposals=False):
    sql = " SELECT MAX(p.Proposal_Id) as Ids, pc.ProposalCode_Id as PCode_Ids, pc.Proposal_Code as PCD " \
          "  FROM Proposal AS p " \
          "    JOIN ProposalCode AS pc ON (p.ProposalCode_Id=pc.ProposalCode_Id) " \
          "    JOIN MultiPartner AS mp ON (p.ProposalCode_Id=mp.ProposalCode_Id) " \
          "    JOIN Partner AS pa ON (mp.Partner_Id=pa.Partner_Id) " \
          "    JOIN Semester AS sm ON (mp.Semester_Id=sm.Semester_Id) " \
          "    JOIN ProposalGeneralInfo AS pgi ON (pgi.ProposalCode_Id=p.ProposalCode_Id) " \
          "    JOIN ProposalInvestigator AS pi ON (pi.ProposalCode_Id=p.ProposalCode_Id) " \
          "  WHERE Phase=1 AND ProposalStatus_Id not in (4, 9, 6, 8, 5, 3, 100) " \
          "     AND CONCAT(sm.Year, '-', sm.Semester) = '{semester}' ".format(semester=semester)

    if partner_code is not None:
        sql = sql + " AND pa.Partner_Code = '{parner_code}' ".format(parner_code=partner_code)

    if proposal_code is not None:
        sql = sql + " AND pc.Proposal_Code = '{proposal_code}' ".format(proposal_code=proposal_code)

    if g.user.user_value == 0:
        return {'ProposalIds': [], 'ProposalCode_Ids': []}

    elif g.user.user_value == 1:
        if len(g.user.tac) > 0:
            partners = [t.partner_id for t in g.user.tac]
            if len(partners) == 1:
                sql = sql + " AND pa.Partner_Id in ({partner_id})".format(partner_id=partners[0])
            else:
                sql = sql + " AND pa.Partner_Id in {partner_id}".format(partner_id=tuple(partners))

        else:
            sql = sql + " AND pi.Investigator_Id = {investigator_id}".format(investigator_id=g.user.user_id)

    sql = sql + " GROUP BY pc.ProposalCode_Id "
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()

    ids = []
    pcode_ids = []
    for index, r in results.iterrows():
        ids.append(r['Ids'])
        pcode_ids.append(r['PCode_Ids'])
    return {'ProposalIds': ids, 'ProposalCode_Ids': pcode_ids}