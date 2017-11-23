
from data.common import Semester as TypeSemester, conn
import pandas as pd
from flask import g





class Proposal:
    @staticmethod
    def get_proposal_ids(**args):
        sql = " SELECT MAX(p.Proposal_Id) as Ids, p.ProposalCode_Id as PCode_Ids " \
              "  FROM Proposal AS p " \
              "    JOIN ProposalCode AS pc ON (p.ProposalCode_Id=pc.ProposalCode_Id) " \
              "    JOIN MultiPartner AS mp ON (p.ProposalCode_Id=mp.ProposalCode_Id) " \
              "    JOIN Partner AS pa ON (mp.Partner_Id=pa.Partner_Id) " \
              "    JOIN ProposalGeneralInfo AS pgi ON (pgi.ProposalCode_Id=p.ProposalCode_Id) " \
              "    JOIN ProposalInvestigator AS pi ON (pi.ProposalCode_Id=p.ProposalCode_Id) " \
              "  WHERE Phase=1 AND ProposalStatus_Id not in (4, 9, 6, 8, 5, 3, 100) "
        if 'semester' in args:
            semester = TypeSemester.get_semester(semester_code=args['semester'])
            sql = sql + " AND mp.Semester_Id = {semester_id} ".format(semester_id=semester.id)

        if 'partner_code' in args and args['partner_code'] is not None:
            sql = sql + "AND pa.Partner_Code = '{parner_code}' ".format(parner_code=args['partner_code'])

        if 'proposal_code' in args and args['proposal_code'] is not None:
            sql = sql + "AND pc.Proposal_Code = '{proposal_code}' ".format(proposal_code=args['proposal_code'])

        if g.user.user_value == 0:
            return {'ProposalIds': [], 'ProposalCodes': []}

        elif g.user.user_value == 1:
            sql = sql + " AND pi.Investigator_Id = {inverstitagor_id}".format(inverstitagor_id=g.user.user_id)

        sql = sql + " GROUP BY pc.ProposalCode_Id "
        results = pd.read_sql(sql, conn)
        ids = [int(x) for x in list(results['Ids'].values)]
        pcode_ids = [int(x) for x in list(results['PCode_Ids'].values)]
        return {'ProposalIds': ids, 'ProposalCodes': pcode_ids}
