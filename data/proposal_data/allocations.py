import pandas as pd
from data import sdb_connect



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


def update_time_allocations(semester, proposals):
    from schema.partner import Partner
    from schema.proposal import ProposalAllocatedTime, TacComment
    all_time_sql = """
       SELECT *
       FROM PriorityAlloc
           join MultiPartner using (MultiPartner_Id)
           join Partner using(Partner_Id)
           join Semester using (Semester_Id)
           join ProposalCode using (ProposalCode_Id)
           left join TacProposalComment using (MultiPartner_Id)
       where Concat(Year, "-", Semester) = "{semester}"
           order by Proposal_Code""".format(semester=semester)

    conn = sdb_connect()
    prev_partner, prev_proposal = '', ''
    for index, row in pd.read_sql(all_time_sql, conn).iterrows():
        partner, proposal = row['Partner_Code'], row["Proposal_Code"]
        pat = ProposalAllocatedTime(
            partner=Partner(
                code=row['Partner_Code'],
                name=row['Partner_Name']
            )
        )
        tac_comments = TacComment(
            partner=Partner(
                code=row['Partner_Code'],
                name=row['Partner_Name']
            ),
            comment=row['TacComment']
        )
        if proposal in proposals:
            if tac_comments not in proposals[proposal].tac_comments:
                proposals[proposal].tac_comments.append(
                    tac_comments
                )

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
                            proposals[proposal].allocated_time[len(proposals[proposal].allocated_time) - 1])
                else:
                    proposals[proposal].allocated_time.append(
                        priority(row['Priority'],
                                 row['TimeAlloc'],
                                 pat
                                 )
                    )
                prev_partner, prev_proposal = partner, proposal
    conn.close()