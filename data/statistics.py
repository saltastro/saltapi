import pandas as pd

from data import sdb_connect
from data.common import get_proposal_ids
from schema.statistics import TimeBreakdown, Statistics


def requested_time(proposal_ids, semester, partner):
    params = dict()
    params["semester"] = semester
    params["proposal_ids"] = proposal_ids
    params["partner_code"] = partner

    sql = """
       SELECT ReqTimeAmount*ReqTimePercent/100.0 as TimePerPartner, Transparency FROM  ProposalCode as pc
           JOIN MultiPartner USING(ProposalCode_Id)
           JOIN Partner USING(Partner_Id)
           JOIN Semester as s  USING (Semester_Id)
           JOIN P1ObservingConditions as oc  ON pc.ProposalCode_Id=oc.ProposalCode_Id
                AND oc.Semester_Id=s.Semester_Id
           JOIN Transparency as t ON oc.Transparency_Id=t.Transparency_Id
        WHERE CONCAT(s.Year, "-", s.Semester)=%(semester)s
           AND pc.ProposalCode_Id IN %(proposal_ids)s
       """
    if partner:
        sql += " AND Partner_Code=%(partner_code)s"
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    conditions = dict()
    for _, row in df.iterrows():
        if not row["Transparency"] in conditions:
            conditions[row["Transparency"]] = 0
        conditions[row["Transparency"]] += row["TimePerPartner"]/3600

    print(conditions)


def proposals(partner_code, semester):
    params = dict()
    params["semester"] = semester

    sql = """
    SELECT DISTINCT pc.ProposalCode_Id as ProposalCode_Id
        FROM ProposalCode AS pc
        JOIN Proposal AS p ON pc.ProposalCode_Id = p.ProposalCode_Id
        JOIN Semester AS s ON p.Semester_Id = s.Semester_Id
        JOIN ProposalInvestigator AS pi ON pc.ProposalCode_Id = pi.ProposalCode_Id
        JOIN Investigator AS i ON pi.Investigator_Id = i.Investigator_Id
        JOIN Institute AS institute ON i.Institute_Id = institute.Institute_Id
        JOIN Partner AS partner ON institute.Partner_Id = partner.Partner_Id
        JOIN P1ObservingConditions AS p1o ON p1o.ProposalCode_Id = p.ProposalCode_Id
    WHERE CONCAT(s.Year, "-", s.Semester)=%(semester)s
    """
    if partner_code:
        params["partner_code"] = partner_code
        sql += " AND Partner_Code=%(partner_code)s"
    codes = list()
    print(sql)
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    for _, row in df.iterrows():
        codes.append(int(row["ProposalCode_Id"]))
    return codes


def time_breakdown(semester):
    # get the filter conditions
    params = dict()
    params["semester"] = semester

    # query for the time breakdown
    sql = """SELECT SUM(ScienceTime) AS ScienceTime, SUM(EngineeringTime) AS EngineeringTime,
    SUM(TimeLostToWeather) AS TimeLostToWeather, SUM(TimeLostToProblems) AS TimeLostToProblems,
    SUM(IdleTime) AS IdleTime
    FROM NightInfo AS ni
    JOIN Semester AS s ON (ni.Date >= s.StartSemester AND ni.Date <= s.EndSemester)
    WHERE CONCAT(s.Year,"-" ,s.Semester)=%(semester)s
    """

    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    return TimeBreakdown(
        science=0 if pd.isnull(df["ScienceTime"][0]) else df["ScienceTime"][0],
        engineering=0 if pd.isnull(df["EngineeringTime"][0]) else df["EngineeringTime"][0],
        lost_to_weather=0 if pd.isnull(df["TimeLostToWeather"][0]) else df["TimeLostToWeather"][0],
        lost_to_problems=0 if pd.isnull(df["TimeLostToProblems"][0]) else df["TimeLostToProblems"][0],
        idle=0 if pd.isnull(df["IdleTime"][0]) else df["IdleTime"][0],
    )


def completion(partner, semester):
    params = dict()
    params["semester"] = semester


    return []


def instruments(partner, semester):
    return []


def target(partner, semester):
    return []


def get_statistics(partner, semester):
    partner = None
    requested_time(get_proposal_ids(semester, partner)["ProposalCode_Ids"], semester, partner)
    get_proposal_ids(semester, partner)
    print(len(get_proposal_ids(semester, partner)["ProposalCode_Ids"]), get_proposal_ids(semester, partner)["ProposalCode_Ids"] )
    return Statistics(
        # completion=completion(partner, semester),
        # instruments=instruments(partner, semester),
        # target=target(partners, semester),
        time_breakdown=time_breakdown(semester)
    )
