import pandas as pd
from data import sdb_connect


def update_time_requirements(data, time_requirements):
    """
    This method add minimum useful time for all semesters it requested times from if any
    it also create an empty array for adding each requested time from a partner

    Parameters
    ----------
    data : pandas data frame
        a query row from proposals query
    time_requirements: array
        time requirements created thus far
    Returns
    -------
    time_requirements : iterable
        updated time requirements
    """
    from schema.proposal import TimeRequirements
    semester = str(data['Year']) + "-" + str(data['Semester'])

    def is_sem_in_time():
        is_in = False
        for t in time_requirements:
            if t.semester == semester:
                is_in = True
        return is_in

    if not is_sem_in_time():
        time_requirements.append(
            TimeRequirements(
                semester=semester,
                minimum_useful_time=None if pd.isnull(data["P1MinimumUsefulTime"]) else data["P1MinimumUsefulTime"],
                time_requests=[]
            )
        )
    return time_requirements


def update_proposals_requested_time(proposal_code_ids):
    """
    Query database for requested times of given proposals ids

    Parameters
    ----------
    proposal_code_ids : string
        proposal code id of interest like '(23, 45, 51, 89, 94)'
    Returns
    -------
    time_requirements : array
        updated time requirements
    """
    time_requirements = {}
    requested_time_sql = """
    SELECT * FROM MultiPartner as mp
        join Semester as sm using (Semester_Id)
        join ProposalCode as pc using (ProposalCode_Id)
        join Partner using (Partner_Id)
        left join P1MinTime as mt on (mt.Semester_Id=sm.Semester_Id and mp.ProposalCode_Id=mt.ProposalCode_Id)
    where mp.ProposalCode_Id in {proposal_code_ids}
        """.format(proposal_code_ids=proposal_code_ids)
    conn = sdb_connect()
    for index, row in pd.read_sql(requested_time_sql, conn).iterrows():
        proposal_code = row['Proposal_Code']
        if proposal_code not in time_requirements:
            time_requirements[proposal_code] = []
        time_requirements[proposal_code] = update_time_requirements(row, time_requirements[proposal_code])
    conn.close()
    return time_requirements


def update_requested_per_partner(proposal_code_ids, proposals):

    """
    Query database for requested times of all partners on the given proposals ids
    and update proposals with query results

    Parameters
    ----------
    proposal_code_ids : string
        proposal code id of interest like '(23, 45, 51, 89, 94)'
    proposals: object
        time requirements created thus far
    Returns
    -------
    None
    """
    from schema.partner import Partner
    from schema.proposal import TimeRequest

    partner_time_sql = """
    SELECT Proposal_Code, ReqTimeAmount*ReqTimePercent/100.0 as TimePerPartner,
        Partner_Id, Partner_Name, Partner_Code, concat(s.Year,'-', s.Semester) as CurSemester
    FROM ProposalCode
        join MultiPartner using (ProposalCode_Id)
        join Semester as s using (Semester_Id)
        join Partner using(Partner_Id)
    WHERE ProposalCode_Id in {proposal_code_ids}
    """.format(proposal_code_ids=proposal_code_ids)

    conn = sdb_connect()
    rq_times = pd.read_sql(partner_time_sql, conn)
    for index, row in rq_times.iterrows():
        try:
            proposal = proposals[row["Proposal_Code"]]
            for p in proposal.time_requirements:
                if p.semester == row['CurSemester']:
                    p.time_requests.append(
                        TimeRequest(
                            partner=Partner(
                                code=row['Partner_Code'],
                                name=row['Partner_Name']
                            ),
                            time=int(row['TimePerPartner'])
                        )
                    )
        except:
            pass

    conn.close()
