from pymysql.connections import Connection
import pandas as pd
from data import sdb_connect
from data.targets import get_targets
from data.instruments import get_instruments
from schema.proposals import Proposal

proposal_data = {}


def query_proposal_data(**args):
    from schema.proposal import Proposals, RequestedTimeM, ProposalInfoM, PI, Distribution
    from schema.instruments import Instruments

    ids = Proposal.get_proposal_ids(**args)
    conn = sdb_connect()
    proposals = {}
    print(ids['ProposalCode_Ids'])

    proposal_sql = " select *,  concat(s.Year, '-', s.Semester) as CurSemester from Proposal as p " \
                   "       join ProposalCode as prc on (prc.ProposalCode_Id = p.ProposalCode_Id) " \
                   "       join ProposalGeneralInfo as pgi on (pgi.ProposalCode_Id = p.ProposalCode_Id) " \
                   "       join P1RequestedTime as p1 using (Proposal_Id) " \
                   "       join Moon as mo on (mo.Moon_Id=p1.Moon_Id) " \
                   "       join ProposalStatus using (ProposalStatus_Id) " \
                   "       join Semester as s on (s.Semester_Id = p1.Semester_Id) " \
                   "       join P1ObservingConditions  as p1o on (p1o.ProposalCode_Id = p.ProposalCode_Id) " \
                   "       left join ProposalText as prt on " \
                   "                (prt.ProposalCode_Id = p.ProposalCode_Id and prt.Semester_Id = s.Semester_Id) " \
                   "       join Transparency using (Transparency_Id) " \
                   "       join ProposalContact as pc on (pc.ProposalCode_Id = p.ProposalCode_Id) " \
                   "       join P1MinTime as p1t on " \
                   "                (p.ProposalCode_Id = p1t.ProposalCode_Id and p1t.Semester_Id = s.Semester_Id) " \
                   " " \
                   "       join Investigator as i on (i.Investigator_Id = pc.Leader_Id) " \
                   "       left join P1Thesis as thesis on (thesis.ProposalCode_Id = p.ProposalCode_Id)" \
                   "       left join ProposalTechReport as pt on (pt.ProposalCode_Id = p.ProposalCode_Id) " \
                   "  where P1RequestedTime > 0  and Proposal_Id in {ids} order by Proposal_Id" \
                   " ".format(ids=tuple(ids['ProposalIds']))
    results = pd.read_sql(proposal_sql, conn)
    conn.close()

    pc = []  # I am using pc to control proposals that are checked
    for index, row in results.iterrows():
        if row["Proposal_Code"] not in proposals:
            proposals[row["Proposal_Code"]] = Proposals(
                id="Proposal: " + str(row["Proposal_Id"]),
                code=row["Proposal_Code"],
                title=row["Title"],
                abstract=row["Abstract"],
                is_p4=row["P4"] == 1,
                status=row["Status"],
                transparency=row["Transparency"],
                max_seeing=row["MaxSeeing"],
                time_requests=[],
                targets=[],
                pi=PI(
                    name=row["FirstName"],
                    surname=row["Surname"],
                    email=row["Email"]
                ),
                instruments=Instruments(
                    rss=[],
                    hrs=[],
                    bvit=[],
                    scam=[]
                ),
                is_thesis=not pd.isnull(row["ThesisType_Id"]),  # concluded that none thesis proposals have null on
                # P1Thesis
                tech_report=row['TechReport']
            )
        proposals[row["Proposal_Code"]].time_requests.append(
            RequestedTimeM(
                minimum_useful_time=row["P1MinimumUsefulTime"],
                semester=str(row['Year']) + "-" + str(row['Semester']),
                distribution=[]
            )
        )

    partner_time_sql = " select Proposal_Code, ReqTimeAmount*ReqTimePercent/100.0 as TimePerPartner, " \
                       "    Partner_Id, Partner_Name, Partner_Code, concat(s.Year,'-', s.Semester) as CurSemester " \
                       "       from ProposalCode  " \
                       "           join MultiPartner using (ProposalCode_Id) " \
                       "           join Semester as s using (Semester_Id) " \
                       "           join Partner using(Partner_Id) " \
                       "  where ProposalCode_Id in {ids}" \
                       " ".format(ids=tuple(ids['ProposalCode_Ids']))
    conn = sdb_connect()
    results = pd.read_sql(partner_time_sql, conn)
    conn.close()

    for index, row in results.iterrows():
        proposal = proposals[row["Proposal_Code"]]

        for p in proposal.time_requests:
            if p.semester == row['CurSemester']:
                p.distribution.append(
                    Distribution(
                        partner_name=row['Partner_Name'],
                        partner_code=row['Partner_Code'],
                        time=int(row['TimePerPartner'])
                    )
                )

    get_instruments(ids, proposals)
    # get_targets(ids=ids, proposals=proposals)

    return proposals.values()


def get_proposals(**args):
    data = query_proposal_data(**args)
    return data
