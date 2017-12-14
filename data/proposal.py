import pandas as pd
from data import sdb_connect
from data.targets import get_targets
from data.instruments import get_instruments
from data.common import get_proposal_ids

proposal_data = {}


def priority(p, time, pat):
    if p == 0:
        pat.p0 = time
    if p == 1:
        pat.p1 = time
    if p == 2:
        pat.p2 = time
    if p == 3:
        pat.p3 = time
    if p == 4:
        pat.p4 = time

    return pat


def make_proposal(row, all_proposals):
    from schema.proposal import Proposals, PI
    from schema.instruments import Instruments
    if all_proposals:
        proposal = Proposals(
            id="Proposal: " + str(row["Proposal_Id"]),
            code=row["Proposal_Code"],
            is_p4=row["P4"] == 1,
            status=row["Status"],
            transparency=row["Transparency"],
            max_seeing=row["MaxSeeing"],
            time_requests=[],
            targets=[],
            allocated_time=[],
            pi=PI(
                name=None,
                surname=None,
                email=None
            ),
            instruments=Instruments(
                rss=[],
                hrs=[],
                bvit=[],
                scam=[]
            ),
            is_thesis=not pd.isnull(row["ThesisType_Id"]),
        )
    else:
        proposal = Proposals(
            id="Proposal: " + str(row["Proposal_Id"]),
            code=row["Proposal_Code"],
            title=row["Title"],
            abstract=row["Abstract"],
            is_p4=row["P4"] == 1,
            status=row["Status"],
            transparency=row["Transparency"],
            max_seeing=row["MaxSeeing"],
            time_requests=[],
            allocated_time=[],
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
            is_thesis=not pd.isnull(row["ThesisType_Id"]),
            tech_report=row['TechReport']
        )

    return proposal


def make_query(ids=None):
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
                   "  where P1RequestedTime > 0 " \
                   " "
    if len(ids['ProposalIds']) == 1:
        proposal_sql += "  and Proposal_Id = {id} order by Proposal_Id".format(id=ids['ProposalIds'][0])
    else:
        proposal_sql += "  and Proposal_Id in {ids} order by Proposal_Id".format(ids=tuple(ids['ProposalIds']))


def query_proposal_data(semester, partner_code=None, proposal_code=None, all_proposals=False):
    from schema.proposal import RequestedTimeM, Distribution, ProposalAllocatedTime

    ids = get_proposal_ids(semester, partner_code=partner_code, proposal_code=proposal_code)
    conn = sdb_connect()
    proposals = {}
    proposal_sql = " select *,  concat(s.Year, '-', s.Semester) as CurSemester from Proposal as p " \
                   "   join ProposalCode as prc on (prc.ProposalCode_Id = p.ProposalCode_Id) " \
                   "   join ProposalGeneralInfo as pgi on (pgi.ProposalCode_Id = p.ProposalCode_Id) " \
                   "   join P1RequestedTime as p1 using (Proposal_Id) " \
                   "   join Moon as mo on (mo.Moon_Id=p1.Moon_Id) " \
                   "   join ProposalStatus using (ProposalStatus_Id) " \
                   "   join Semester as s on (s.Semester_Id = p1.Semester_Id) " \
                   "   join P1ObservingConditions  as p1o on (p1o.ProposalCode_Id = p.ProposalCode_Id) " \
                   "   left join ProposalText as prt on " \
                   "            (prt.ProposalCode_Id = p.ProposalCode_Id and prt.Semester_Id = s.Semester_Id) " \
                   "   join Transparency using (Transparency_Id) " \
                   "   join ProposalContact as pc on (pc.ProposalCode_Id = p.ProposalCode_Id) " \
                   "   join P1MinTime as p1t on " \
                   "                (p.ProposalCode_Id = p1t.ProposalCode_Id and p1t.Semester_Id = s.Semester_Id) " \
                   " " \
                   "   join Investigator as i on (i.Investigator_Id = pc.Leader_Id) " \
                   "   left join P1Thesis as thesis on (thesis.ProposalCode_Id = p.ProposalCode_Id)" \
                   "   left join ProposalTechReport as pt on (pt.ProposalCode_Id = p.ProposalCode_Id) " \
                   "  where P1RequestedTime > 0 "
    if len(ids['ProposalIds']) == 1:
        proposal_sql += "  and Proposal_Id = {id} order by Proposal_Id".format(id=ids['ProposalIds'][0])
    else:
        proposal_sql += "  and Proposal_Id in {ids} order by Proposal_Id".format(ids=tuple(ids['ProposalIds']))
    results = pd.read_sql(proposal_sql, conn)
    conn.close()

    for index, row in results.iterrows():
        if row["Proposal_Code"] not in proposals:
            proposals[row["Proposal_Code"]] = make_proposal(row, all_proposals)
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
                       "           join Partner using(Partner_Id) "
    if len(ids['ProposalIds']) == 1:
        partner_time_sql += "  where ProposalCode_Id = {id}".format(id=ids['ProposalCode_Ids'][0])
    else:
        partner_time_sql += "  where ProposalCode_Id in {ids}".format(ids=tuple(ids['ProposalCode_Ids']))
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
    get_targets(ids=ids, proposals=proposals)

    all_time_sql = 'SELECT * FROM PriorityAlloc ' \
                   '    join MultiPartner using (MultiPartner_Id) ' \
                   '    join Partner using(Partner_Id) ' \
                   '    join Semester using (Semester_Id) ' \
                   '    join ProposalCode using (ProposalCode_Id)' \
                   ' where Concat(Year, "-", Semester) = "{semester}" order by Proposal_Code'.format(semester=semester)

    conn = sdb_connect()
    alloc_results = pd.read_sql(all_time_sql, conn)
    conn.close()

    for index, row in alloc_results.iterrows():
        partner, proposal = row['Partner_Code'], row["Proposal_Code"]
        pat = ProposalAllocatedTime(
            partner_code=row['Partner_Code'],
            partner_name=row['Partner_Name']
        )
        if proposal in proposals:
            if len(proposals[proposal].allocated_time) == 0:
                proposals[proposal].allocated_time.append(
                        priority(row['Priority'],
                                 row['TimeAlloc'],
                                 pat
                                 )
                    )
                prev_partner, prev_proposal = partner, proposal
            else:
                if partner == prev_partner and proposal == prev_proposal:
                        proposals[proposal].allocated_time[len(proposals[proposal].allocated_time) - 1] = \
                            priority(
                                row['Priority'],
                                row['TimeAlloc'],
                                proposals[proposal].allocated_time[len(proposals[proposal].allocated_time)-1])
                else:
                    proposals[proposal].allocated_time.append(
                        priority(row['Priority'],
                                 row['TimeAlloc'],
                                 pat
                                 )
                    )
                prev_partner, prev_proposal = partner, proposal

    return proposals.values()


def get_proposals(**args):
    data = query_proposal_data(**args)
    return data
