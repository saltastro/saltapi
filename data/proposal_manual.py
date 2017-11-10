import pandas as pd
from data import conn
from schema.proposals import Proposal

proposal_data = {}


def query_proposal_data(**args):
    from schema.proposal_manual import ProposalM, RequestedTimeM, ProposalInfoM
    ids = Proposal.get_proposal_ids(**args)
    print(tuple(ids['ProposalIds']))
    sql = " select * from Proposal " \
          "     join ProposalCode using (ProposalCode_Id) " \
          "     join ProposalGeneralInfo using (ProposalCode_Id) " \
          "     join P1RequestedTime as p1 using (Proposal_Id) " \
          "     join Moon as mo on (mo.Moon_Id=p1.Moon_Id) " \
          "     join ProposalStatus using (ProposalStatus_Id) " \
          "     join Semester as s on (s.Semester_Id = p1.Semester_Id) " \
          "     join P1ObservingConditions  using (ProposalCode_Id) " \
          "     join Transparency using (Transparency_Id) " \
          "     join ProposalContact as pc using(ProposalCode_Id) " \
          "     join Investigator as i on(i.Investigator_Id = pc.Leader_Id) " \
          "  where Proposal_Id in {ids} " \
          " ".format(ids=tuple(ids['ProposalIds']))
    results = pd.read_sql(sql, conn)
    times = []
    p = []
    pc = []
    for index, row in results.iterrows():
        if row["Proposal_Code"] not in pc:
            times = []
            p.append(ProposalM(
                proposal_id="Proposal: " + str(row["Proposal_Id"]),
                proposal_code=row["Proposal_Code"],
                general_info=ProposalInfoM(
                    is_p4=row["P4"] == 1,
                    status=row["Status"],
                    transparency=row["Transparency"],
                    max_seeing=row["MaxSeeing"]
                ),
                total_time_requested=row["TotalReqTime"],
                requester_time=[],
                is_new=False
            ))
        p[len(p) - 1].requester_time.append(RequestedTimeM(
            moon=row["Moon"],
            time=row["P1RequestedTime"],
            for_semester=str(row['Year']) + "-" + str(row['Semester'])
        ))
        pc.append(row["Proposal_Code"])
    return p


def get_proposals(**args):
    data = query_proposal_data(**args)
    return data
