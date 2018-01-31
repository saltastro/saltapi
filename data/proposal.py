import os
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


def make_proposal(row, ids, text):
    from schema.proposal import Proposals, PI, SALTAstronomer
    from schema.instruments import Instruments

    title = text[row["Proposal_Code"]]["title"] if row["Title"] is None else row["Title"]
    abstract = text[row["Proposal_Code"]]["abstract"]if row["Abstract"] is None else row["Abstract"]
    sa = SALTAstronomer(
                name=row["SAFname"],
                surname=row["SASname"],
                email=row["SAEmail"],
                username=row["SAUsername"]) if row["SAFname"] is not None else None

    if row["Proposal_Id"] in ids["ProposalIds"]:
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
            tac_comment=[],
            pi=PI(
                name=None,
                surname=None,
                email=None
            ),
            S_a_l_t_astronomer=SALTAstronomer(
                name=row["SAFname"],
                surname=row["SASname"],
                email=row["SAEmail"],
                username=row["SAUsername"],
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
            title=title,
            abstract=abstract,
            is_p4=row["P4"] == 1,
            status=row["Status"],
            transparency=row["Transparency"],
            max_seeing=row["MaxSeeing"],
            time_requests=[],
            allocated_time=[],
            targets=[],
            tac_comment=[],
            pi=PI(
                name=row["PIFname"],
                surname=row["PISname"],
                email=row["PIEmail"]
            ),
            instruments=Instruments(
                rss=[],
                hrs=[],
                bvit=[],
                scam=[]
            ),
            is_thesis=not pd.isnull(row["ThesisType_Id"]),
            tech_report=row['TechReport'],
            S_a_l_t_astronomer=sa,
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


def query_proposal_data(semester, partner_code=None, all_proposals=False):
    from schema.proposal import RequestedTimeM, Distribution, ProposalAllocatedTime, TacComment

    ids = get_proposal_ids(semester, partner_code=partner_code)

    proposals = {}
    proposals_text = {}
    proposal_sql = """
                    select *,  concat(s.Year, '-', s.Semester) as CurSemester,
                            i.FirstName as PIFname, i.Surname as PISname, i.Email as PIEmail,
                            tsa.FirstName as SAFname, tsa.Surname as SASname, tsa.Email as SAEmail,
                            sau.Username as SAUsername
                        from Proposal as p
                            join ProposalCode as prc on (prc.ProposalCode_Id = p.ProposalCode_Id)
                            join ProposalGeneralInfo as pgi on (pgi.ProposalCode_Id = p.ProposalCode_Id)
                            join P1RequestedTime as p1 using (Proposal_Id)
                            join Moon as mo on (mo.Moon_Id=p1.Moon_Id)
                            join ProposalStatus using (ProposalStatus_Id)
                            join Semester as s on (s.Semester_Id = p1.Semester_Id)
                            join P1ObservingConditions  as p1o on (p1o.ProposalCode_Id = p.ProposalCode_Id)
                            left join ProposalText as prt on
                                (prt.ProposalCode_Id = p.ProposalCode_Id and prt.Semester_Id = s.Semester_Id)
                            join Transparency using (Transparency_Id)
                            join ProposalContact as pc on (pc.ProposalCode_Id = p.ProposalCode_Id)
                            join P1MinTime as p1t on
                                   (p.ProposalCode_Id = p1t.ProposalCode_Id and p1t.Semester_Id = s.Semester_Id)
                            join Investigator as i on (i.Investigator_Id = pc.Leader_Id)
                            left join P1Thesis as thesis on (thesis.ProposalCode_Id = p.ProposalCode_Id)
                            left join ProposalTechReport as pt on (pt.ProposalCode_Id = p.ProposalCode_Id and pt.Semester_Id = s.Semester_Id)
                            left join Investigator as tsa on (tsa.Investigator_Id = pc.Astronomer_Id)
                            left join PiptUser as sau on (sau.Investigator_Id = pc.Astronomer_Id)
                        where P1RequestedTime > 0 AND CONCAT(s.Year, '-', s.Semester) = \"{semester}\"
                     """.format(semester=semester)

    proposals_text_sql = """
                    SELECT * FROM ProposalText
                        join ProposalCode using(ProposalCode_Id)
                    WHERE ProposalCode_Id in ({ids})
                        order by Semester_Id desc """.format(ids=', '.join(ids['ProposalCode_Ids']))
    conn = sdb_connect()
    for index, row in pd.read_sql(proposals_text_sql, conn).iterrows():
        if row["Proposal_Code"] not in proposals_text:
            proposals_text[row["Proposal_Code"]] = {
                "title": row["Title"], "abstract": row["Abstract"]
            }
    conn.close()

    conn = sdb_connect()
    if all_proposals:
        proposal_sql += "  AND Proposal_Id IN ({ids}) order by Proposal_Id".format(ids=', '.join(ids['all_proposals']))
        results = pd.read_sql(proposal_sql, conn)
    else:
        proposal_sql += "  AND Proposal_Id IN ({ids}) order by Proposal_Id".format(ids=', '.join(ids['ProposalIds']))
        results = pd.read_sql(proposal_sql, conn)
    conn.close()
    for index, row in results.iterrows():
        if row["Proposal_Code"] not in proposals:
            proposals[row["Proposal_Code"]] = make_proposal(row, ids, proposals_text)
        proposals[row["Proposal_Code"]].time_requests.append(
            RequestedTimeM(
                minimum_useful_time=row["P1MinimumUsefulTime"],
                semester=str(row['Year']) + "-" + str(row['Semester']),
                distribution=[]
            )
        )
    partner_time_sql = """
                        SELECT Proposal_Code, ReqTimeAmount*ReqTimePercent/100.0 as TimePerPartner, 
                           Partner_Id, Partner_Name, Partner_Code, concat(s.Year,'-', s.Semester) as CurSemester 
                              from ProposalCode  
                                  join MultiPartner using (ProposalCode_Id) 
                                  join Semester as s using (Semester_Id) 
                                  join Partner using(Partner_Id) 
                         WHERE ProposalCode_Id in ({ids})
                       """.format(ids=', '.join(ids['ProposalCode_Ids']))

    conn = sdb_connect()
    for index, row in pd.read_sql(partner_time_sql, conn).iterrows():
        try:
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
        except KeyError:
            pass
    conn.close()

    get_instruments(ids, proposals)
    get_targets(ids=ids, proposals=proposals)

    all_time_sql = """
            SELECT * FROM PriorityAlloc
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
            partner_code=row['Partner_Code'],
            partner_name=row['Partner_Name']
        )
        tac_comment = TacComment(
                    partner_code=row['Partner_Code'],
                    comment=row['TacComment']
                )
        if proposal in proposals:
            if tac_comment not in proposals[proposal].tac_comment:
                proposals[proposal].tac_comment.append(
                    tac_comment
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
                                proposals[proposal].allocated_time[len(proposals[proposal].allocated_time)-1])
                else:
                    proposals[proposal].allocated_time.append(
                        priority(row['Priority'],
                                 row['TimeAlloc'],
                                 pat
                                 )
                    )
                prev_partner, prev_proposal = partner, proposal
    conn.close()

    return proposals.values()


def get_proposals(**args):
    data = query_proposal_data(**args)
    return data


def liaison_astronomer(proposal_code):
    """
    The liaison astronomer for a proposal. The astronomer's username is returned.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-007".

    Returns
    -------
    username : str
        The liaison astronomer's username.

    """
    sql = '''SELECT PiptUser.Username AS LiaisonAstronomer
       FROM PiptUser
       RIGHT JOIN Investigator USING (PiptUser_Id)
       RIGHT JOIN ProposalContact ON Investigator.Investigator_Id = ProposalContact.Astronomer_Id
       RIGHT JOIN ProposalCode USING (ProposalCode_Id)
       WHERE ProposalCode.Proposal_Code=%s'''
    df = pd.read_sql(sql, params=(proposal_code,), con=sdb_connect())

    return df['LiaisonAstronomer'][0]


def reviewer(proposal_code):
    """
    The reviewer for a proposal. The reviewer's username is returned.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-007".

    Returns
    -------
    username : str
        The reviewer's username.

    """
    sql = '''SELECT PiptUser.Username AS Reviewer
       FROM PiptUser
       RIGHT JOIN Investigator USING (PiptUser_Id)
       RIGHT JOIN ProposalTechReport ON Investigator.Investigator_Id = ProposalTechReport.Astronomer_Id
       RIGHT JOIN ProposalCode USING (ProposalCode_Id)
       WHERE ProposalCode.Proposal_Code=%s'''
    df = pd.read_sql(sql, params=(proposal_code,), con=sdb_connect())

    return df['Reviewer'][0]


def is_investigator(username, proposal_code):
    """
    Check whether a user is investigator on a proposal.

    Parameters
    ----------
    username : str
        The username.
    proposal_code : str
        The proposal code, such as "2018-1-SCI-007".

    Returns
    -------
    isinvestigator : bool
        Whether the user is an investigator on the proposal.
    """

    sql = '''
SELECT COUNT(*) AS Count
       FROM ProposalContact AS ProposalContact
       JOIN ProposalCode ON ProposalContact.ProposalCode_Id = ProposalCode.ProposalCode_Id
       JOIN Investigator ON ProposalContact.Astronomer_Id = Investigator.Investigator_Id
       JOIN PiptUser ON Investigator.PiptUser_Id = PiptUser.PiptUser_Id
WHERE ProposalCode.Proposal_Code = %s AND PiptUser.Username = %s
'''
    conn = sdb_connect()
    df = pd.read_sql(sql, conn, params=(proposal_code, username))
    conn.close()

    return df['Count'][0] > 0


def latest_version(proposal_code, phase):
    """
    The latest version number of a proposal, given a proposal phase.

    This function requires the environment variable PROPOSALS_DIR to exist. Its value must be the absolute file path
    to the directory containing all the proposal content.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-009".
    phase : int
        The proposal phase (1 or 2).

    Returns
    -------
    version : number
        The current version number.
    """

    sql = '''
SELECT Proposal.Submission AS Submission
       FROM Proposal
       JOIN ProposalCode ON Proposal.ProposalCode_Id = ProposalCode.ProposalCode_Id
WHERE ProposalCode.Proposal_Code = %s AND Proposal.Phase = %s
ORDER BY Proposal.Submission DESC
LIMIT 1
'''
    conn = sdb_connect()
    df = pd.read_sql(sql, conn, params=(proposal_code, phase))
    conn.close()

    if not len(df['Submission']):
        raise Exception('Proposal {proposal_code} does not have any submitted version for phase {phase}'
                        .format(proposal_code=proposal_code, phase=phase))

    return df['Submission'][0]


def summary_file(proposal_code):
    """
    The file path of a proposal's summary file.

    Parameters
    ----------
    proposal_code : str
        The proposal code, such as "2018-1-SCI-005".

    Returns
    -------
    filepath : str
        The file path of the summary.
    """

    return os.path.join(os.environ['PROPOSALS_DIR'],
                        proposal_code,
                        str(latest_version(proposal_code, 1)),
                        'Summary.pdf')
