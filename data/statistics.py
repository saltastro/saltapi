import pandas as pd
from flask import g

from data import sdb_connect
from data.common import proposal_code_ids_for_statistics
from schema.statistics import TimeBreakdown, Statistics, ObservingConditions, CloudCondition, TransparencyDistribution, \
    SeeingDistribution, SeeingCondition, StatisticsTarget, InstrumentStatistics, Instruments, DetectorMode, ExposureMode, \
    CompletionStatistics, TimeSummary, Priorities, ObservingMode, ProposalStatistics
from schema.user import RoleType
from util.semester import query_semester_id


class PriorityValue:
    p0 = 0
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0

    def add_to_priority(self, value, priority):
        if priority == 0:
            self.p0 += value
        if priority == 1:
            self.p1 += value
        if priority == 2:
            self.p2 += value
        if priority == 3:
            self.p3 += value
        if priority == 4:
            self.p4 += value


def number_of_proposals_per_cloud_conditions(proposal_code_ids, semester, partner):
    params = dict()
    params["semester"] = semester
    params["proposal_code_ids"] = proposal_code_ids
    params["partner_code"] = partner

    sql = """
       SELECT ReqTimeAmount*ReqTimePercent/100.0 as TimeForPartner, Transparency FROM  ProposalCode as pc
           JOIN MultiPartner USING(ProposalCode_Id)
           JOIN Partner USING(Partner_Id)
           JOIN Semester as s  USING (Semester_Id)
           JOIN P1ObservingConditions as oc  ON pc.ProposalCode_Id=oc.ProposalCode_Id
                AND oc.Semester_Id=s.Semester_Id
           JOIN Transparency as t ON oc.Transparency_Id=t.Transparency_Id
        WHERE CONCAT(s.Year, "-", s.Semester)=%(semester)s
           AND pc.ProposalCode_Id IN %(proposal_code_ids)s
       """
    if partner:
        sql += " AND Partner_Code=%(partner_code)s"
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    counts = dict()
    for _, row in df.iterrows():
        if not row["Transparency"] in counts:
            counts[row["Transparency"]] = 0
        counts[row["Transparency"]] += 1

    return TransparencyDistribution(
        any=0 if "Any" not in counts else counts["Any"],
        clear=0 if "Clear" not in counts else counts["Clear"],
        thick_cloud=0 if "Thick cloud" not in counts else counts["Thick cloud"],
        thin_cloud=0 if "Thin cloud" not in counts else counts["Thin cloud"],
    )


def share_percentage(semester_id):
    params = dict()
    params["semester_id"] = semester_id
    sql = """
        SELECT Partner_Code, SharePercent
        FROM PartnerShareTimeDist AS pst
            JOIN Semester AS s ON pst.Semester_Id = s.Semester_Id
            JOIN Partner AS partner ON pst.Partner_Id = partner.Partner_Id
        WHERE s.Semester_Id=%(semester_id)s
    """
    share = dict()
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    for _, row in df.iterrows():
        share[row["Partner_Code"]] = row["SharePercent"]
    return share


def transparency_statistics(proposal_code_ids, semester, partner):
    params = dict()
    params["semester"] = semester
    params["proposal_code_ids"] = proposal_code_ids
    params["partner_code"] = partner

    sql = """
       SELECT ReqTimeAmount*ReqTimePercent/100.0 as TimeForPartner, Transparency, MaxSeeing FROM  ProposalCode as pc
           JOIN MultiPartner USING(ProposalCode_Id)
           JOIN Partner USING(Partner_Id)
           JOIN Semester as s  USING (Semester_Id)
           JOIN P1ObservingConditions as oc  ON pc.ProposalCode_Id=oc.ProposalCode_Id
                AND oc.Semester_Id=s.Semester_Id
           JOIN Transparency as t ON oc.Transparency_Id=t.Transparency_Id
        WHERE CONCAT(s.Year, "-", s.Semester)=%(semester)s
           AND pc.ProposalCode_Id IN %(proposal_code_ids)s
       """
    if partner:
        sql += " AND Partner_Code=%(partner_code)s"
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    cloud_times = dict()
    cloud_counts = dict()
    for _, row in df.iterrows():
        if row["Transparency"] not in cloud_times:
            cloud_times[row["Transparency"]] = 0
            cloud_counts[row["Transparency"]] = 0
        cloud_times[row["Transparency"]] += row["TimeForPartner"]/3600
        cloud_counts[row["Transparency"]] += 1

    def get_seeing_range(max_seeing):
        if max_seeing < 0:
            raise ValueError("Maximum seeing is less than zero.")
        if max_seeing <= 1.5:
            return "less_equal_1_dot_5"
        if max_seeing <= 2:
            return "less_equal_2"
        if max_seeing <= 3:
            return "less_equal_3"
        if max_seeing > 3:
            return "more_than_3"
        raise ValueError("Unsupported seeing value")
    seeing_times = dict()
    seeing_counts = dict()
    for _, row in df.iterrows():
        seeing_range = get_seeing_range(row["MaxSeeing"])
        if seeing_range not in seeing_times:
            seeing_times[seeing_range] = 0
            seeing_counts[seeing_range] = 0
        seeing_times[seeing_range] += row["TimeForPartner"]/3600
        seeing_counts[seeing_range] += 1

    return {
        "time_request": TransparencyDistribution(
            any=0 if "Any" not in cloud_times else cloud_times["Any"],
            clear=0 if "Clear" not in cloud_times else cloud_times["Clear"],
            thick_cloud=0 if "Thick cloud" not in cloud_times else cloud_times["Thick cloud"],
            thin_cloud=0 if "Thin cloud" not in cloud_times else cloud_times["Thin cloud"],
        ),
        "time_request_per_seeing": SeeingDistribution(
            less_equal_1_dot_5=0 if "less_equal_1_dot_5" not in seeing_times else seeing_times["less_equal_1_dot_5"],
            less_equal_2=0 if "less_equal_2" not in seeing_times else seeing_times["less_equal_2"],
            less_equal_3=0 if "less_equal_3" not in seeing_times else seeing_times["less_equal_3"],
            more_than_3=0 if "more_than_3" not in seeing_times else seeing_times["more_than_3"],
        ),
        "number_of_proposals": TransparencyDistribution(
            any=0 if "Any" not in cloud_counts else cloud_counts["Any"],
            clear=0 if "Clear" not in cloud_counts else cloud_counts["Clear"],
            thick_cloud=0 if "Thick cloud" not in cloud_counts else cloud_counts["Thick cloud"],
            thin_cloud=0 if "Thin cloud" not in cloud_counts else cloud_counts["Thin cloud"],
        ),
        "number_of_proposals_per_seeing": SeeingDistribution(
            less_equal_1_dot_5=0 if "less_equal_1_dot_5" not in seeing_counts else seeing_counts["less_equal_1_dot_5"],
            less_equal_2=0 if "less_equal_2" not in seeing_counts else seeing_counts["less_equal_2"],
            less_equal_3=0 if "less_equal_3" not in seeing_counts else seeing_counts["less_equal_3"],
            more_than_3=0 if "more_than_3" not in seeing_counts else seeing_counts["more_than_3"],
        )
    }


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


def allocated_time_per_priority(semester):
    params = dict()
    params["semester_id"] = query_semester_id(semester)
    
    allocated = dict()
    sql = """
    SELECT SUM(TimeAlloc) as TotalAllocations, Partner_Code, Priority FROM PriorityAlloc
        JOIN MultiPartner USING (MultiPartner_Id)
        JOIN Partner USING(Partner_Id)
        JOIN Semester USING(Semester_Id)
    WHERE Semester_Id=%(semester_id)s
    GROUP BY Priority, Partner_Code
            """
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    for _, row in df.iterrows():
        if row["Partner_Code"] not in allocated:
            allocated[row["Partner_Code"]] = PriorityValue()
        allocated[row["Partner_Code"]].add_to_priority(row["TotalAllocations"], row["Priority"])
    return allocated


def observed_time_per_proposal(proposal_code_ids, semester):
    params = dict()
    params["semester_id"] = query_semester_id(semester)
    params["proposal_code_ids"] = proposal_code_ids
    proposal_observed = dict()
    sql = """
    SELECT
        BlockVisit_Id,
        Partner_Code,
        TimeAlloc,
        Proposal_Code,
        ObsTime,
        b.Priority as BlockPriority,
        pa.Priority as AllocPriority
           FROM BlockVisit AS bv
           JOIN Block AS b ON bv.Block_Id = b.Block_Id
           JOIN ProposalCode AS pc ON b.ProposalCode_Id = pc.ProposalCode_Id
           JOIN Proposal using(Proposal_Id)
           JOIN MultiPartner as mp ON (pc.ProposalCode_Id = mp.ProposalCode_Id )
           JOIN Partner USING(Partner_Id)
           JOIN PriorityAlloc as pa USING (MultiPartner_Id)
    WHERE pc.ProposalCode_Id IN %(proposal_code_ids)s
            AND BlockVisitStatus_Id = 1
            AND Proposal.Semester_Id = %(semester_id)s and mp.Semester_Id = %(semester_id)s
        """

    df = pd.read_sql(sql, con=sdb_connect(), params=params)

    for _, row in df.iterrows():
        if row["Proposal_Code"] not in proposal_observed:
            proposal_observed[row["Proposal_Code"]] = {
                "block_visit": dict(),
                "allocated_time": dict()
            }
        proposal_observed[row["Proposal_Code"]]["block_visit"][row["BlockVisit_Id"]] = {
            "priority": row["BlockPriority"],
            "time": row["ObsTime"]
        }

        if row["Partner_Code"] not in proposal_observed[row["Proposal_Code"]]["allocated_time"]:
            proposal_observed[row["Proposal_Code"]]["allocated_time"][row["Partner_Code"]] = dict()
        proposal_observed[row["Proposal_Code"]]["allocated_time"][row["Partner_Code"]][row["AllocPriority"]] = \
            row["TimeAlloc"]
    return proposal_observed


def sum_observed_for_partner(proposal_observed):
    
    observed = dict()
    for proposal_code, observed in proposal_observed.items():

        observed_time = PriorityValue()  #
        alloc_total = PriorityValue()  # Allocated time for the proposal from all the partners per priority
        for block_id, obz_time in observed["block_visit"].items():
            observed_time.add_to_priority(obz_time["time"], obz_time["priority"])

        for partner_code, allocations in observed["allocated_time"].items():
            alloc_total.add_to_priority(allocations[0], 0)
            alloc_total.add_to_priority(allocations[1], 1)
            alloc_total.add_to_priority(allocations[2], 2)
            alloc_total.add_to_priority(allocations[3], 3)
            alloc_total.add_to_priority(allocations[4], 4)

        for partner_code, allocations in observed["allocated_time"].items():
            if partner_code not in observed:
                observed[partner_code] = PriorityValue()
            if alloc_total.p0 > 0:
                observed[partner_code].add_to_priority(observed_time.p0 * allocations[0] / alloc_total.p0, 0)
            if alloc_total.p1 > 0:
                observed[partner_code].add_to_priority(observed_time.p1 * allocations[1] / alloc_total.p1, 1)
            if alloc_total.p2 > 0:
                observed[partner_code].add_to_priority(observed_time.p2 * allocations[2] / alloc_total.p2, 2)
            if alloc_total.p3 > 0:
                observed[partner_code].add_to_priority(observed_time.p3 * allocations[3] / alloc_total.p3, 3)
            if alloc_total.p4 > 0:
                observed[partner_code].add_to_priority(observed_time.p4 * allocations[4] / alloc_total.p4, 4)
    return observed


def create_completion_stats(observed, allocated, share, partner):
    sum_of_all_partners = {
        "allocated": PriorityValue(),
        "observed": PriorityValue(),
        "share_percentage": 0
    }
    temp_completion = []
    for partner_code, time in allocated.items():
        if not partner_code == "ALL":
            if partner_code not in observed:
                observed[partner_code] = PriorityValue()
            sum_of_all_partners["allocated"].add_to_priority(time.p0, 0)
            sum_of_all_partners["allocated"].add_to_priority(time.p1, 1)
            sum_of_all_partners["allocated"].add_to_priority(time.p2, 2)
            sum_of_all_partners["allocated"].add_to_priority(time.p3, 3)
            sum_of_all_partners["allocated"].add_to_priority(time.p4, 4)

            sum_of_all_partners["observed"].add_to_priority(observed[partner_code].p0, 0)
            sum_of_all_partners["observed"].add_to_priority(observed[partner_code].p1, 1)
            sum_of_all_partners["observed"].add_to_priority(observed[partner_code].p2, 2)
            sum_of_all_partners["observed"].add_to_priority(observed[partner_code].p3, 3)
            sum_of_all_partners["observed"].add_to_priority(observed[partner_code].p4, 4)

            sum_of_all_partners["share_percentage"] += share[partner_code]

        temp_completion.append(
            CompletionStatistics(
                partner=partner_code,
                summary=TimeSummary(
                    allocated_time=Priorities(
                        p0=time.p0,
                        p1=time.p1,
                        p2=time.p2,
                        p3=time.p3,
                        p4=time.p4
                    ),
                    observed_time=Priorities(
                        p0=observed[partner_code].p0,
                        p1=observed[partner_code].p1,
                        p2=observed[partner_code].p2,
                        p3=observed[partner_code].p3,
                        p4=observed[partner_code].p4
                    )
                ),
                share_percentage=share[partner_code]
            )
        )
    # Adding total for all
    temp_completion.append(
        CompletionStatistics(
            partner="ALL",
            share_percentage=sum_of_all_partners["share_percentage"],
            summary=TimeSummary(
                allocated_time=Priorities(
                    p0=sum_of_all_partners["allocated"].p0,
                    p1=sum_of_all_partners["allocated"].p1,
                    p2=sum_of_all_partners["allocated"].p2,
                    p3=sum_of_all_partners["allocated"].p3,
                    p4=sum_of_all_partners["allocated"].p4
                ),
                observed_time=Priorities(
                    p0=sum_of_all_partners["observed"].p0,
                    p1=sum_of_all_partners["observed"].p1,
                    p2=sum_of_all_partners["observed"].p2,
                    p3=sum_of_all_partners["observed"].p3,
                    p4=sum_of_all_partners["observed"].p4
                )
            )
        )
    )
    if partner:
        res = []
        for c in temp_completion:
            if c.partner == partner or c.partner == "ALL":
                res.append(c)
        if g.user.has_role(RoleType.ADMINISTRATOR) \
                or g.user.has_role(RoleType.BOARD)\
                or g.user.has_role(RoleType.TAC_CHAIR, partner) or g.user.has_role(RoleType.TAC_MEMBER, partner):
            return res
        return []
    else:
        if g.user.has_role(RoleType.ADMINISTRATOR) or g.user.has_role(RoleType.BOARD):
            return temp_completion
        else:
            res = []
            for r in g.user.role:
                if r.type == RoleType.TAC_CHAIR:
                    for c in temp_completion:
                        if c.partner in r.partners or c.partner == "ALL":
                            res.append(c)
                if r.type == RoleType.TAC_MEMBER:
                    for c in temp_completion:
                        if c.partner in r.partners:
                            res.append(c)
            return res


def completion(partner, semester):
    proposal_code_ids = proposal_code_ids_for_statistics(semester)
    params = dict()
    params["semester_id"] = query_semester_id(semester)
    params["proposal_code_ids"] = proposal_code_ids

    allocated = allocated_time_per_priority(semester)

    observed_proposals = observed_time_per_proposal(proposal_code_ids, semester)

    observed = sum_observed_for_partner(observed_proposals)
    share = share_percentage(params["semester_id"])

    return create_completion_stats(observed, allocated, share, partner)


def instruments_statistics(proposal_code_ids, partner, semester):
    params = dict()
    params["proposal_code_ids"] = proposal_code_ids
    params["semester"] = semester
    params["partner"] = partner

    sql = """
SELECT
    Mode as RSSMode,
    P1Bvit_Id,
    P1Hrs_Id,
    P1Rss_Id,
    P1Salticam_Id,
    ExposureMode,
    sc.DetectorMode AS SCAMDetectorMode,
    rs.DetectorMode AS RSSDetectorMode
FROM P1Config
    JOIN ProposalCode USING(ProposalCode_Id)
        LEFT JOIN P1Rss USING(P1Rss_Id)
        LEFT JOIN RssDetectorMode AS rs USING(RssDetectorMode_Id)
        LEFT JOIN RssMode USING(RssMode_Id)
        LEFT JOIN P1RssSpectroscopy USING(P1RssSpectroscopy_Id)
        LEFT JOIN RssGrating USING(RssGrating_Id)
        LEFT JOIN P1RssFabryPerot USING(P1RssFabryPerot_Id)
        LEFT JOIN RssFabryPerotMode USING(RssFabryPerotMode_Id)
        LEFT JOIN RssEtalonConfig USING(RssEtalonConfig_Id)
        LEFT JOIN P1RssPolarimetry USING(P1RssPolarimetry_Id)
        LEFT JOIN RssPolarimetryPattern USING(RssPolarimetryPattern_Id)
        LEFT JOIN P1RssMask USING(P1RssMask_Id)
        LEFT JOIN RssMaskType USING(RssMaskType_Id)
        LEFT JOIN P1Salticam USING(P1Salticam_Id)
        LEFT JOIN SalticamDetectorMode AS sc USING(SalticamDetectorMode_Id)
        LEFT JOIN P1Bvit USING(P1Bvit_Id)
        LEFT JOIN BvitFilter USING(BvitFilter_Id)
        LEFT JOIN P1Hrs USING(P1Hrs_Id)
        LEFT JOIN HrsMode USING(HrsMode_Id)
WHERE ProposalCode_Id IN %(proposal_code_ids)s
               """
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    total_count = {
        "bvit": 0,
        "hrs": 0,
        "scam": 0,
        "rss": 0,
        "rss_detector": {
            "Drift Scan": 0,
            "FRAME TRANSFER": 0,
            "NORMAL": 0,
            "Shuffle": 0,
            "SLOT MODE": 0,
        },
        "salticam_detector": {
            "DRIFTSCAN": 0,
            "NORMAL": 0,
            "FRAME XFER": 0,
            "SLOT": 0,
        },
        "hrs_resolution": {
            "HIGH RESOLUTION": 0,
            "HIGH STABILITY": 0,
            "INT CAL FIBRE": 0,
            "LOW RESOLUTION": 0,
            "MEDIUM RESOLUTION": 0,
        },
        "rss_observing_mode": {
            "Fabry Perot": 0,
            "FP polarimetry": 0,
            "Imaging": 0,
            "MOS polarimetry": 0,
            "MOS": 0,
            "Polarimetric imaging": 0,
            "Spectroscopy": 0,
            "Spectropolarimetry": 0,
        }
    }

    def count_instrument_data(row_data):
        if not pd.isnull(row_data["P1Bvit_Id"]):
            total_count["bvit"] += 1
        if not pd.isnull(row_data["P1Hrs_Id"]):
            total_count["hrs"] += 1
        if not pd.isnull(row_data["P1Salticam_Id"]):
            total_count["scam"] += 1
        if not pd.isnull(row_data["P1Rss_Id"]):
            total_count["rss"] += 1
        if not pd.isnull(row_data["RSSDetectorMode"]):
            total_count["rss_detector"][row_data["RSSDetectorMode"]] += 1
        if not pd.isnull(row_data["SCAMDetectorMode"]):
            total_count["salticam_detector"][row_data["SCAMDetectorMode"]] += 1
        if not pd.isnull(row_data["ExposureMode"]):
            total_count["hrs_resolution"][row_data["ExposureMode"]] += 1
        if not pd.isnull(row_data["P1Rss_Id"]) and not pd.isnull(row_data["RSSMode"]):
            total_count["rss_observing_mode"][row_data["RSSMode"]] += 1

    for _, row in df.iterrows():
        count_instrument_data(row)

    sql = """
    SELECT
        P1Rss_Id,
        Mode as RSSMode,
        P1Hrs_Id,
        P1Salticam_Id,
        P1Bvit_Id,
        ExposureMode,
        sc.DetectorMode AS SCAMDetectorMode,
        rs.DetectorMode AS RSSDetectorMode,
        (ReqTimeAmount*ReqTimePercent/100.0)/3600 as TimeForPartner
    FROM P1Config
        JOIN MultiPartner USING(ProposalCode_Id)
        JOIN Semester USING (Semester_Id)
        JOIN Partner USING (Partner_Id)
        LEFT JOIN P1Rss USING(P1Rss_Id)
        LEFT JOIN RssDetectorMode AS rs USING(RssDetectorMode_Id)
        LEFT JOIN RssMode USING(RssMode_Id)
        LEFT JOIN P1RssSpectroscopy USING(P1RssSpectroscopy_Id)
        LEFT JOIN RssGrating USING(RssGrating_Id)
        LEFT JOIN P1RssFabryPerot USING(P1RssFabryPerot_Id)
        LEFT JOIN RssFabryPerotMode USING(RssFabryPerotMode_Id)
        LEFT JOIN RssEtalonConfig USING(RssEtalonConfig_Id)
        LEFT JOIN P1RssPolarimetry USING(P1RssPolarimetry_Id)
        LEFT JOIN RssPolarimetryPattern USING(RssPolarimetryPattern_Id)
        LEFT JOIN P1RssMask USING(P1RssMask_Id)
        LEFT JOIN RssMaskType USING(RssMaskType_Id)
        LEFT JOIN P1Salticam USING(P1Salticam_Id)
        LEFT JOIN SalticamDetectorMode AS sc USING(SalticamDetectorMode_Id)
        LEFT JOIN P1Bvit USING(P1Bvit_Id)
        LEFT JOIN BvitFilter USING(BvitFilter_Id)
        LEFT JOIN P1Hrs USING(P1Hrs_Id)
        LEFT JOIN HrsMode USING(HrsMode_Id)
    WHERE  CONCAT(Year,"-" ,Semester)=%(semester)s
        AND ProposalCode_Id IN %(proposal_code_ids)s

    """
    if partner:
        sql += " AND Partner_Code = %(partner)s"
    sql += " GROUP BY ProposalCode_Id, Partner_Id"
    final_time = {
        "bvit": 0,
        "hrs": 0,
        "scam": 0,
        "rss": 0,
        "rss_detector": {
            "Drift Scan": 0,
            "FRAME TRANSFER": 0,
            "NORMAL": 0,
            "Shuffle": 0,
            "SLOT MODE": 0,
        },
        "salticam_detector": {
            "DRIFTSCAN": 0,
            "NORMAL": 0,
            "FRAME XFER": 0,
            "SLOT": 0,
        },
        "hrs_resolution": {
            "HIGH RESOLUTION": 0,
            "HIGH STABILITY": 0,
            "INT CAL FIBRE": 0,
            "LOW RESOLUTION": 0,
            "MEDIUM RESOLUTION": 0,
        },
        "rss_observing_mode": {
            "Fabry Perot": 0,
            "FP polarimetry": 0,
            "Imaging": 0,
            "MOS polarimetry": 0,
            "MOS": 0,
            "Polarimetric imaging": 0,
            "Spectroscopy": 0,
            "Spectropolarimetry": 0,
        }
    }
    df = pd.read_sql(sql, con=sdb_connect(), params=params)

    def count_instrument_time(row_data):
        if not pd.isnull(row_data["P1Bvit_Id"]):
            final_time["bvit"] += row_data["TimeForPartner"]
        if not pd.isnull(row_data["P1Hrs_Id"]):
            final_time["hrs"] += row_data["TimeForPartner"]
        if not pd.isnull(row_data["P1Salticam_Id"]):
            final_time["scam"] += row_data["TimeForPartner"]
        if not pd.isnull(row_data["P1Rss_Id"]):
            final_time["rss"] += row_data["TimeForPartner"]

        if not pd.isnull(row_data["RSSDetectorMode"]):
            final_time["rss_detector"][row_data["RSSDetectorMode"]] += row_data["TimeForPartner"]

        if not pd.isnull(row_data["P1Rss_Id"]) and not pd.isnull(row_data["RSSMode"]):
            final_time["rss_observing_mode"][row_data["RSSMode"]] += row_data["TimeForPartner"]

        if not pd.isnull(row_data["SCAMDetectorMode"]):
            final_time["salticam_detector"][row_data["SCAMDetectorMode"]] += row_data["TimeForPartner"]
        if not pd.isnull(row_data["ExposureMode"]):
            final_time["hrs_resolution"][row_data["ExposureMode"]] += row_data["TimeForPartner"]

    for _, row in df.iterrows():
        count_instrument_time(row)

    return InstrumentStatistics(
        time_requested_per_instrument=Instruments(
            bvit=final_time["bvit"],
            hrs=final_time["hrs"],
            salticam=final_time["scam"],
            rss=final_time["rss"]
        ),
        number_of_configurations_per_instrument=Instruments(
            bvit=total_count["bvit"],
            hrs=total_count["hrs"],
            salticam=total_count["scam"],
            rss=total_count["rss"]
        ),
        time_requested_per_rss_detector_mode=DetectorMode(
            drift_scan=final_time["rss_detector"]["Drift Scan"],
            frame_transfer=final_time["rss_detector"]["FRAME TRANSFER"],
            normal=final_time["rss_detector"]["NORMAL"],
            shuffle=final_time["rss_detector"]["Shuffle"],
            slot_mode=final_time["rss_detector"]["SLOT MODE"],
        ),


        number_of_configurations_per_rss_detector_mode=DetectorMode(
            drift_scan=total_count["rss_detector"]["Drift Scan"],
            frame_transfer=total_count["rss_detector"]["FRAME TRANSFER"],
            normal=total_count["rss_detector"]["NORMAL"],
            shuffle=total_count["rss_detector"]["Shuffle"],
            slot_mode=total_count["rss_detector"]["SLOT MODE"],
        ),
        time_requested_per_salticam_detector_mode=DetectorMode(
            drift_scan=final_time["salticam_detector"]["DRIFTSCAN"],
            frame_transfer=final_time["salticam_detector"]["FRAME XFER"],
            normal=final_time["salticam_detector"]["NORMAL"],
            slot_mode=final_time["salticam_detector"]["SLOT"]
        ),
        number_of_configurations_per_salticam_detector_mode=DetectorMode(
            drift_scan=total_count["salticam_detector"]["DRIFTSCAN"],
            frame_transfer=total_count["salticam_detector"]["FRAME XFER"],
            normal=total_count["salticam_detector"]["NORMAL"],
            slot_mode=total_count["salticam_detector"]["SLOT"]
        ),
        time_requested_per_hrs_resolution=ExposureMode(
            low_resolution=final_time["hrs_resolution"]["LOW RESOLUTION"],
            medium_resolution=final_time["hrs_resolution"]["MEDIUM RESOLUTION"],
            high_resolution=final_time["hrs_resolution"]["HIGH RESOLUTION"],
            high_stability=final_time["hrs_resolution"]["HIGH STABILITY"],
            int_cal_fibre=final_time["hrs_resolution"]["INT CAL FIBRE"]
        ),
        number_of_configurations_per_hrs_resolution=ExposureMode(
            low_resolution=total_count["hrs_resolution"]["LOW RESOLUTION"],
            medium_resolution=total_count["hrs_resolution"]["MEDIUM RESOLUTION"],
            high_resolution=total_count["hrs_resolution"]["HIGH RESOLUTION"],
            high_stability=total_count["hrs_resolution"]["HIGH STABILITY"],
            int_cal_fibre=total_count["hrs_resolution"]["INT CAL FIBRE"]
        ),
        time_requested_per_rss_observing_mode=ObservingMode(
            fabry_perot=final_time["rss_observing_mode"]["Fabry Perot"],
            fabry_perot_polarimetry=final_time["rss_observing_mode"]["FP polarimetry"],
            mos=final_time["rss_observing_mode"]["MOS"],
            mos_polarimetry=final_time["rss_observing_mode"]["MOS polarimetry"],
            imaging=final_time["rss_observing_mode"]["Imaging"],
            polarimetric_imaging=final_time["rss_observing_mode"]["Polarimetric imaging"],
            spectropolarimetry=final_time["rss_observing_mode"]["Spectropolarimetry"],
            spectroscopy=final_time["rss_observing_mode"]["Spectroscopy"],
        ),
        number_of_configurations_per_rss_observing_mode=ObservingMode(
            fabry_perot=total_count["rss_observing_mode"]["Fabry Perot"],
            fabry_perot_polarimetry=total_count["rss_observing_mode"]["FP polarimetry"],
            mos=total_count["rss_observing_mode"]["MOS"],
            mos_polarimetry=total_count["rss_observing_mode"]["MOS polarimetry"],
            imaging=total_count["rss_observing_mode"]["Imaging"],
            polarimetric_imaging=total_count["rss_observing_mode"]["Polarimetric imaging"],
            spectropolarimetry=total_count["rss_observing_mode"]["Spectropolarimetry"],
            spectroscopy=total_count["rss_observing_mode"]["Spectroscopy"],
        )
    )


def targets(proposal_code_ids):
    params = dict()
    params["proposal_code_ids"] = proposal_code_ids

    sql = """
        SELECT distinct RaH, RaM, RaS, DecD, DecM, DecS, DecSign, Optional
        FROM Proposal
            JOIN P1ProposalTarget USING (ProposalCode_Id)
            JOIN Target USING (Target_Id)
            JOIN TargetCoordinates USING(TargetCoordinates_Id)
        WHERE ProposalCode_Id IN %(proposal_code_ids)s
           """
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    all_targets = []
    for _, row in df.iterrows():
        sign = -1 if row['DecSign'] == '-' else 1
        all_targets.append(
            StatisticsTarget(
                is_optional=row['Optional'] == 1,
                right_ascension=(row['RaH'] + row['RaM'] / 60 + row['RaS'] / 3600) / (24 / 360),
                declination=(sign * (row['DecD'] + row['DecM'] / 60 + row['DecS'] / 3600)),
            )
        )
    return all_targets


def clouds_conditions(proposal_code_ids, partner, semester):
    stats = transparency_statistics(proposal_code_ids, semester, partner)
    return {
        "clouds": CloudCondition(
            time_requested=stats["time_request"],
            number_of_proposals=stats["number_of_proposals"]
        ),
        "seeing": SeeingCondition(
            time_requested=stats["time_request_per_seeing"],
            number_of_proposals=stats["number_of_proposals_per_seeing"]
        )
    }


def observing_conditions(proposal_code_ids, partner, semester):
    xx = clouds_conditions(proposal_code_ids, partner, semester)
    return ObservingConditions(
        clouds=xx["clouds"],
        seeing=xx["seeing"]
    )


def proposal_statistics(proposal_code_ids, semester):
    params = dict()
    params["proposal_code_ids"] = proposal_code_ids
    params["semester_id"] = query_semester_id(semester)
    sql = """
SELECT Proposal_Code, ThesisType_Id, CONCAT(Year, "-", Semester) as Semester, P4 FROM Proposal
    JOIN ProposalCode USING(ProposalCode_Id)
    JOIN ProposalGeneralInfo USING(ProposalCode_Id)
    JOIN MultiPartner USING(ProposalCode_Id)
    JOIN Semester ON(Semester.Semester_Id=MultiPartner.Semester_Id)
    LEFT JOIN P1Thesis USING(ProposalCode_Id)
WHERE Current=1
    AND Proposal.Semester_Id=%(semester_id)s
    AND ProposalCode_Id IN %(proposal_code_ids)s
    """
    proposals = dict()
    new_proposals = 0
    long_term_proposals = 0
    new_long_term_proposals = 0
    thesis_proposals = 0
    p4_proposals = 0

    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    for _, row in df.iterrows():
        if not row["Proposal_Code"] in proposals:
            proposals[row["Proposal_Code"]] = {
                "semesters": [],
                "is_thesis": None,
                "is_p4": None
            }
        proposals[row["Proposal_Code"]]["is_p4"] = True if row["P4"] == 1 else False
        proposals[row["Proposal_Code"]]["is_thesis"] = True if row["ThesisType_Id"] and row["ThesisType_Id"] > 0 else False
        if row["Semester"] not in proposals[row["Proposal_Code"]]["semesters"]:
            proposals[row["Proposal_Code"]]["semesters"].append(row["Semester"])

    for p in proposals.items():
        if not any([s < semester for s in p[1]["semesters"]]):
            new_proposals += 1
            if len(p[1]["semesters"]) > 1:
                new_long_term_proposals += 1
        if len(p[1]["semesters"]) > 1:
            long_term_proposals += 1
        if p[1]["is_p4"]:
            p4_proposals += 1
        if p[1]["is_thesis"]:
            thesis_proposals += 1

    return ProposalStatistics(
        number_of_proposals=len(proposal_code_ids),
        new_proposals=new_proposals,
        long_term_proposals=long_term_proposals,
        new_long_term_proposals=new_long_term_proposals,
        thesis_proposals=thesis_proposals,
        p4_proposals=p4_proposals
    )


def get_statistics(partner, semester):
    proposal_code_ids = proposal_code_ids_for_statistics(semester, partner)
    return Statistics(
        completion=completion(partner, semester),
        instruments_statistics=instruments_statistics(proposal_code_ids, partner, semester),
        observing_conditions=observing_conditions(proposal_code_ids, partner, semester),
        proposal_statistics=proposal_statistics(proposal_code_ids, semester),
        targets=targets(proposal_code_ids),
        time_breakdown=time_breakdown(semester)
    )
