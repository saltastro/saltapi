from pymysql.connections import Connection
import pandas as pd
from data import sdb_connect
from data.instruments import get_instruments
from schema.proposals import Proposal

proposal_data = {}


def query_proposal_data(**args):
    from schema.proposal import Proposals, RequestedTimeM, ProposalInfoM, PI
    from schema.instruments import RSS, HRS, BVIT, SCAM, Instruments, Spectroscopy, Polarimetry, FabryPerot, Mask

    ids = Proposal.get_proposal_ids(**args)
    conn = sdb_connect()
    proposals = {}
    try:
        proposal_sql = " select *,  concat(s.Year, '-', s.Semester) as CurSemester from Proposal " \
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
                   "     join ProposalText using(ProposalCode_Id) " \
                   "     join P1MinTime using(ProposalCode_Id) " \
                   "     left join P1Thesis using (ProposalCode_Id) " \
                   "     join ProposalCode using (ProposalCode_Id) " \
                   "  where Proposal_Id in {ids} order by Proposal_Id" \
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
                    semester=row["CurSemester"],
                    abstract=row["Abstract"],
                    minimum_useful_time=row["P1MinimumUsefulTime"],
                    general_info=ProposalInfoM(
                        is_p4=row["P4"] == 1,
                        status=row["Status"],
                        transparency=row["Transparency"],
                        max_seeing=row["MaxSeeing"]
                    ),
                    total_time_requested=row["TotalReqTime"],
                    time_requests=[],
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
                    is_thesis=not pd.isnull(row["ThesisType_Id"])  # concluded that none thesis proposals have null on
                    # P1Thesis
                )
            proposals[row["Proposal_Code"]].time_requests.append(
                RequestedTimeM(
                    moon=row["Moon"],
                    time=row["P1RequestedTime"],
                    for_semester=str(row['Year']) + "-" + str(row['Semester'])
                )
            )  # I am using pc to control proposals that are checked

    except:
        # TODO: Log exception
        raise RuntimeError("Failed to get Proposal data")

    get_instruments(ids, proposals)
    return proposals.values()


def get_proposals(**args):
    data = query_proposal_data(**args)
    return data
