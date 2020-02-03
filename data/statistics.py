import pandas as pd
from flask import g
from collections import defaultdict

from data import sdb_connect
from data.common import proposal_code_ids_for_statistics
from schema.statistics import TimeBreakdown, Statistics, ObservingConditions, TransparencyCondition, TransparencyDistribution, \
    SeeingDistribution, SeeingCondition, StatisticsTarget, InstrumentStatistics, Instruments, DetectorMode, Resolution, \
    CompletionStatistics, TimeSummary, Priorities, ObservingMode, ProposalStatistics
from schema.user import RoleType
from util.semester import query_semester_id


class PriorityValues:
    """
    Priority and its values
    """
    p0 = 0
    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0

    def add_to_priority(self, value, priority):
        """
        Add value to given priority

        :param value: float
            The value to add
        :param priority: int
            The priority adding value too.
        :return: None
        """
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
        if priority < 0 or priority > 4 or not isinstance(priority, int):
            raise ValueError("Priority is integer between 0 and 4")


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
    counts = defaultdict(int)
    for _, row in df.iterrows():
        counts[row["Transparency"]] += 1

    return TransparencyDistribution(
        any=counts.get("Any", 0),
        clear=counts.get("Clear", 0),
        thick_cloud=counts.get("Thick cloud", 0),
        thin_cloud=counts.get("Thin cloud", 0),
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


def transparency_and_seeing_statistics(proposal_code_ids, semester, partner):
    """
    Calculate the statistics of observing conditions per seeing and transparency return how they have been distributed.

    :param proposal_code_ids: list
        List of proposal code ids
    :param semester: str
        The semester
    :param partner: str
        The partner code
    :return: ObservingConditions
        The observing conditions
    """
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
    cloud_times = defaultdict(int)
    cloud_counts = defaultdict(int)
    for _, row in df.iterrows():
        cloud_times[row["Transparency"]] += row["TimeForPartner"]/3600
        cloud_counts[row["Transparency"]] += 1

    def get_seeing_range(max_seeing):
        if max_seeing < 0:
            raise ValueError("Maximum seeing is less than zero.")
        if max_seeing <= 1.5:
            return "less_equal_1_dot_5"
        if max_seeing <= 2:
            return "less_equal_2"
        if max_seeing <= 2.5:
            return "less_equal_2_dot_5"
        if max_seeing <= 3:
            return "less_equal_3"
        if max_seeing > 3:
            return "more_than_3"
        raise ValueError("Unsupported seeing value")
    seeing_times = defaultdict(int)
    seeing_counts = defaultdict(int)

    for _, row in df.iterrows():
        seeing_range = get_seeing_range(row["MaxSeeing"])
        seeing_times[seeing_range] += row["TimeForPartner"]/3600
        seeing_counts[seeing_range] += 1

    return {
        "time_request_per_transparency": TransparencyDistribution(
            any=cloud_times.get("Any", 0),
            clear=cloud_times.get("Clear", 0),
            thick_cloud=cloud_times.get("Thick cloud", 0),
            thin_cloud=cloud_times.get("Thin cloud", 0)
        ),
        "time_request_per_seeing": SeeingDistribution(
            less_equal_1_dot_5=seeing_times.get("less_equal_1_dot_5", 0),
            less_equal_2=seeing_times.get("less_equal_2", 0),
            less_equal_2_dot_5=seeing_times.get("less_equal_2_dot_5", 0),
            less_equal_3=seeing_times.get("less_equal_3", 0),
            more_than_3=seeing_times.get("more_than_3", 0)
        ),
        "number_of_proposals_per_transparency": TransparencyDistribution(
            any=cloud_counts.get("Any", 0),
            clear=cloud_counts.get("Clear", 0),
            thick_cloud=cloud_counts.get("Thick cloud", 0),
            thin_cloud=cloud_counts.get("Thin cloud", 0)
        ),
        "number_of_proposals_per_seeing": SeeingDistribution(
            less_equal_1_dot_5=seeing_counts.get("less_equal_1_dot_5", 0),
            less_equal_2=seeing_counts.get("less_equal_2", 0),
            less_equal_2_dot_5=seeing_counts.get("less_equal_2_dot_5", 0),
            less_equal_3=seeing_counts.get("less_equal_3", 0),
            more_than_3=seeing_counts.get("more_than_3", 0)
        )
    }


def time_breakdown(semester):
    # get the filter parameters
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
    SELECT SUM(TimeAlloc) as TotalAllocation, Partner_Code, Priority FROM PriorityAlloc
        JOIN MultiPartner USING (MultiPartner_Id)
        JOIN Partner USING(Partner_Id)
        JOIN Semester USING(Semester_Id)
    WHERE Semester_Id=%(semester_id)s
    GROUP BY Priority, Partner_Code
            """
    df = pd.read_sql(sql, con=sdb_connect(), params=params)
    for _, row in df.iterrows():
        if row["Partner_Code"] not in allocated:
            allocated[row["Partner_Code"]] = PriorityValues()
        allocated[row["Partner_Code"]].add_to_priority(row["TotalAllocation"], row["Priority"])
    return allocated


def proposal_observed_time(proposal_code_ids, semester):
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


def sum_observed_and_allocated_time_for_partner(proposal_observed):
    
    observed = defaultdict(lambda: PriorityValues())
    for proposal_code, observation in proposal_observed.items():

        observed_time = PriorityValues()  #
        alloc_total = PriorityValues()  # Allocated time for the proposal from all the partners per priority
        for block_id, obz_time in observation["block_visit"].items():
            observed_time.add_to_priority(obz_time["time"], obz_time["priority"])

        for partner_code, allocations in observation["allocated_time"].items():
            alloc_total.add_to_priority(allocations[0], 0)
            alloc_total.add_to_priority(allocations[1], 1)
            alloc_total.add_to_priority(allocations[2], 2)
            alloc_total.add_to_priority(allocations[3], 3)
            alloc_total.add_to_priority(allocations[4], 4)

        for partner_code, allocations in observation["allocated_time"].items():
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


def partners_time_summary(allocated, observed, share):
    time_summary = []
    all_partners_time_summary = {
        "allocated": PriorityValues(),
        "observed": PriorityValues(),
        "share_percentage": 0
    }
    for partner_code, time in allocated.items():
        if not partner_code == "ALL":
            if partner_code not in observed:
                observed[partner_code] = PriorityValues()
            all_partners_time_summary["allocated"].add_to_priority(time.p0, 0)
            all_partners_time_summary["allocated"].add_to_priority(time.p1, 1)
            all_partners_time_summary["allocated"].add_to_priority(time.p2, 2)
            all_partners_time_summary["allocated"].add_to_priority(time.p3, 3)
            all_partners_time_summary["allocated"].add_to_priority(time.p4, 4)

            all_partners_time_summary["observed"].add_to_priority(observed[partner_code].p0, 0)
            all_partners_time_summary["observed"].add_to_priority(observed[partner_code].p1, 1)
            all_partners_time_summary["observed"].add_to_priority(observed[partner_code].p2, 2)
            all_partners_time_summary["observed"].add_to_priority(observed[partner_code].p3, 3)
            all_partners_time_summary["observed"].add_to_priority(observed[partner_code].p4, 4)

            all_partners_time_summary["share_percentage"] += share[partner_code]

        time_summary.append(
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
    time_summary.append(
        CompletionStatistics(
            partner="ALL",
            share_percentage=all_partners_time_summary["share_percentage"],
            summary=TimeSummary(
                allocated_time=Priorities(
                    p0=all_partners_time_summary["allocated"].p0,
                    p1=all_partners_time_summary["allocated"].p1,
                    p2=all_partners_time_summary["allocated"].p2,
                    p3=all_partners_time_summary["allocated"].p3,
                    p4=all_partners_time_summary["allocated"].p4
                ),
                observed_time=Priorities(
                    p0=all_partners_time_summary["observed"].p0,
                    p1=all_partners_time_summary["observed"].p1,
                    p2=all_partners_time_summary["observed"].p2,
                    p3=all_partners_time_summary["observed"].p3,
                    p4=all_partners_time_summary["observed"].p4
                )
            )
        )
    )
    return time_summary


def create_completion_stats(observed, allocated, share, partner):

    all_time_summaries = partners_time_summary(allocated, observed, share)
    if partner:
        time_summaries = []
        for c in all_time_summaries:
            if c.partner == partner or c.partner == "ALL":
                time_summaries.append(c)
        if g.user.has_role(RoleType.ADMINISTRATOR) \
                or g.user.has_role(RoleType.BOARD)\
                or g.user.has_role(RoleType.TAC_CHAIR, partner) or g.user.has_role(RoleType.TAC_MEMBER, partner):
            return time_summaries
        return []
    else:
        if g.user.has_role(RoleType.ADMINISTRATOR) or g.user.has_role(RoleType.BOARD):
            return all_time_summaries
        else:
            time_summaries = []
            for r in g.user.role:
                if r.type == RoleType.TAC_CHAIR:
                    for c in all_time_summaries:
                        if c.partner in r.partners or c.partner == "ALL":
                            time_summaries.append(c)
                if r.type == RoleType.TAC_MEMBER:
                    for c in all_time_summaries:
                        if c.partner in r.partners:
                            time_summaries.append(c)
            return time_summaries


def completion(partner, semester):
    proposal_code_ids = proposal_code_ids_for_statistics(semester)
    params = dict()
    params["semester_id"] = query_semester_id(semester)
    params["proposal_code_ids"] = proposal_code_ids

    allocated = allocated_time_per_priority(semester)

    observed_proposals = proposal_observed_time(proposal_code_ids, semester)

    observed = sum_observed_and_allocated_time_for_partner(observed_proposals)
    share = share_percentage(params["semester_id"])

    return create_completion_stats(observed, allocated, share, partner)


def proposal_configurations(data):
    """
    Create a dict as with a proposal code as a key, instrument configurations and requested time per partner.

    :param data: DataFrame
        Instruments query results
    :return: dict
        Proposal and it's instrument configuration
    """
    proposals = dict()

    def _instrument_counter(row_data):

        proposals[row_data["Proposal_Code"]]["time_requested_pp"][row_data["Partner_Code"]] = row_data["TimeForPartner"]


        if not pd.isnull(row_data["P1Bvit_Id"]):
            proposals[row_data["Proposal_Code"]]["is_bvit"] = True
        if not pd.isnull(row_data["P1Hrs_Id"]):
            proposals[row_data["Proposal_Code"]]["is_hrs"] = True
        if not pd.isnull(row_data["P1Salticam_Id"]):
            proposals[row_data["Proposal_Code"]]["is_scam"] = True
        if not pd.isnull(row_data["P1Rss_Id"]):
            proposals[row_data["Proposal_Code"]]["is_rss"] = True

        if not pd.isnull(row_data["RSSDetectorMode"]):
            proposals[row_data["Proposal_Code"]]["rss_detector_modes"].add(row_data["RSSDetectorMode"])

        if not pd.isnull(row_data["P1Rss_Id"]) and not pd.isnull(row_data["RSSMode"]):
            proposals[row_data["Proposal_Code"]]["rss_observing_modes"].add(row_data["RSSMode"])
        if not pd.isnull(row_data["SCAMDetectorMode"]):
            proposals[row_data["Proposal_Code"]]["scam_detector_modes"].add(row_data["SCAMDetectorMode"])
        if not pd.isnull(row_data["HRSResolution"]):
            proposals[row_data["Proposal_Code"]]["hrs_resolutions"].add(row_data["HRSResolution"])

    for _, row in data.iterrows():
        if row["Proposal_Code"] not in proposals:
            proposals[row["Proposal_Code"]] = {
                "is_bvit": False,
                "is_hrs": False,
                "is_rss": False,
                "is_scam": False,
                "hrs_resolutions": set([]),
                "rss_observing_modes": set([]),
                "scam_detector_modes": set([]),
                "rss_detector_modes": set([]),
                "time_requested_pp": dict(),
            }
        _instrument_counter(row)
    return proposals


def instruments_statistics_count(proposal_conf, partner):
    """
    Count number of configurations per instrument and mode and how much time is requested per instrument and mode.

    :param proposal_conf: dict
        The proposal and it's instrument configuration
    :param partner: str
        The partner code
    :return: dict
        The instruments statistics
    """
    stats = {
        "bvit_total": 0,
        "bvit_requested_total": 0,
        "hrs_total": 0,
        "hrs_requested_total": 0,
        "scam_total": 0,
        "scam_requested_total": 0,
        "rss_total": 0,
        "rss_requested_total": 0,
        "rss_detector_mode_total": defaultdict(int),
        "rss_detector_mode_requested_total": defaultdict(int),
        "scam_detector_mode_total": defaultdict(int),
        "scam_detector_mode_requested_total": defaultdict(int),
        "hrs_resolution_total": defaultdict(int),
        "hrs_resolution_requested_total": defaultdict(int),
        "rss_observing_mode_total": defaultdict(int),
        "rss_observing_mode_requested_total": defaultdict(int)
    }

    def _get_requested_total(requested_times):
        requested_total = 0
        for partner_code, time in requested_times.items():
            if partner:
                if partner == partner_code:
                    requested_total += time
            else:
                requested_total += time
        return requested_total

    for _, data in proposal_conf.items():
        total_requested = _get_requested_total(data["time_requested_pp"])
        if data["is_bvit"]:
            stats["bvit_total"] += 1
            stats["bvit_requested_total"] += total_requested

        if data["is_hrs"]:

            stats["hrs_total"] += 1
            stats["hrs_requested_total"] += total_requested

            # data["hrs_resolutions"] is a set of so a given resolution so it is guaranteed to have only
            # one resolution type per proposal
            for resolution in data["hrs_resolutions"]:
                stats["hrs_resolution_requested_total"][resolution] += total_requested
                stats["hrs_resolution_total"][resolution] += 1

        if data["is_rss"]:
            stats["rss_total"] += 1
            stats["rss_requested_total"] += total_requested

            # data["rss_detector_modes"] is a set of a given detector mode so it is guaranteed to have only
            # one detector modes type per proposal
            for detector_mode in data["rss_detector_modes"]:
                stats["rss_detector_mode_requested_total"][detector_mode] += total_requested
                stats["rss_detector_mode_total"][detector_mode] += 1

            # data["rss_observing_modes"] is a set of a given observing mode so it is guaranteed to have only
            # one observing mode type per proposal
            for observing_mode in data["rss_observing_modes"]:
                stats["rss_observing_mode_requested_total"][observing_mode] += total_requested
                stats["rss_observing_mode_total"][observing_mode] += 1
                
        if data["is_scam"]:
            stats["scam_total"] += 1
            stats["scam_requested_total"] += total_requested

            # data["scam_detector_modes"] is a set of a given detector mode so it is guaranteed to have only
            # one detector modes type per proposal
            for detector_mode in data["scam_detector_modes"]:
                stats["scam_detector_mode_requested_total"][detector_mode] += total_requested
                stats["scam_detector_mode_total"][detector_mode] += 1

    return stats


def instruments_statistics(proposal_code_ids, partner, semester):
    params = dict()
    params["proposal_code_ids"] = proposal_code_ids
    params["semester"] = semester
    params["partner"] = partner

    sql = """
SELECT
    Proposal_Code,
    Partner_Code,
    Mode as RSSMode,
    P1Hrs_Id,
    P1Rss_Id,
    P1Salticam_Id,
    P1Bvit_Id,
    ExposureMode as HRSResolution,
    sc.DetectorMode AS SCAMDetectorMode,
    rs.DetectorMode AS RSSDetectorMode,
    (ReqTimeAmount*ReqTimePercent/100.0)/3600 as TimeForPartner
FROM P1Config
    JOIN ProposalCode USING(ProposalCode_Id)
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
    df = pd.read_sql(sql, con=sdb_connect(), params=params)

    proposal_conf = proposal_configurations(df)

    instruments_stats_count = instruments_statistics_count(proposal_conf, partner)

    return InstrumentStatistics(
        bvit_total=instruments_stats_count["bvit_total"],
        bvit_requested_total=instruments_stats_count["bvit_requested_total"],

        hrs_total=instruments_stats_count["hrs_total"],
        hrs_requested_total=instruments_stats_count["hrs_requested_total"],
        hrs_resolution_total=Resolution(
            low_resolution=instruments_stats_count["hrs_resolution_total"].get("LOW RESOLUTION", 0),
            medium_resolution=instruments_stats_count["hrs_resolution_total"].get("MEDIUM RESOLUTION", 0),
            high_resolution=instruments_stats_count["hrs_resolution_total"].get("HIGH RESOLUTION", 0),
            high_stability=instruments_stats_count["hrs_resolution_total"].get("HIGH STABILITY", 0),
            int_cal_fibre=instruments_stats_count["hrs_resolution_total"].get("INT CAL FIBRE", 0),
        ),
        hrs_resolution_requested_total=Resolution(
            low_resolution=instruments_stats_count["hrs_resolution_requested_total"].get("LOW RESOLUTION", 0),
            medium_resolution=instruments_stats_count["hrs_resolution_requested_total"].get("MEDIUM RESOLUTION", 0),
            high_resolution=instruments_stats_count["hrs_resolution_requested_total"].get("HIGH RESOLUTION", 0),
            high_stability=instruments_stats_count["hrs_resolution_requested_total"].get("HIGH STABILITY", 0),
            int_cal_fibre=instruments_stats_count["hrs_resolution_requested_total"].get("INT CAL FIBRE", 0),
        ),

        rss_total=instruments_stats_count["rss_total"],
        rss_requested_total=instruments_stats_count["rss_requested_total"],

        rss_detector_mode_total=DetectorMode(
            drift_scan=instruments_stats_count["rss_detector_mode_total"].get("DRIFT SCAN", 0),
            frame_transfer=instruments_stats_count["rss_detector_mode_total"].get("FRAME TRANSFER", 0),
            normal=instruments_stats_count["rss_detector_mode_total"].get("NORMAL", 0),
            shuffle=instruments_stats_count["rss_detector_mode_total"].get("SHUFFLE", 0),
            slot_mode=instruments_stats_count["rss_detector_mode_total"].get("SLOT MODE", 0)
        ),
        rss_detector_mode_requested_total=DetectorMode(
            drift_scan=instruments_stats_count["rss_detector_mode_requested_total"].get("DRIFT SCAN", 0),
            frame_transfer=instruments_stats_count["rss_detector_mode_requested_total"].get("FRAME TRANSFER", 0),
            normal=instruments_stats_count["rss_detector_mode_requested_total"].get("NORMAL", 0),
            shuffle=instruments_stats_count["rss_detector_mode_requested_total"].get("SHUFFLE", 0),
            slot_mode=instruments_stats_count["rss_detector_mode_requested_total"].get("SLOT MODE", 0)
        ),

        rss_observing_mode_total=ObservingMode(
            fabry_perot=instruments_stats_count["rss_observing_mode_total"].get("Fabry Perot", 0),
            fabry_perot_polarimetry=instruments_stats_count["rss_observing_mode_total"].get("FP polarimetry", 0),
            mos=instruments_stats_count["rss_observing_mode_total"].get("MOS", 0),
            mos_polarimetry=instruments_stats_count["rss_observing_mode_total"].get("MOS polarimetry", 0),
            imaging=instruments_stats_count["rss_observing_mode_total"].get("Imaging", 0),
            polarimetric_imaging=instruments_stats_count["rss_observing_mode_total"].get("Polarimetric imaging", 0),
            spectropolarimetry=instruments_stats_count["rss_observing_mode_total"].get("Spectropolarimetry", 0),
            spectroscopy=instruments_stats_count["rss_observing_mode_total"].get("Spectroscopy", 0)
        ),
        rss_observing_mode_requested_total=ObservingMode(
            fabry_perot=instruments_stats_count["rss_observing_mode_requested_total"].get("Fabry Perot", 0),
            fabry_perot_polarimetry=instruments_stats_count["rss_observing_mode_requested_total"].get("FP polarimetry", 0),
            mos=instruments_stats_count["rss_observing_mode_requested_total"].get("MOS", 0),
            mos_polarimetry=instruments_stats_count["rss_observing_mode_requested_total"].get("MOS polarimetry", 0),
            imaging=instruments_stats_count["rss_observing_mode_requested_total"].get("Imaging", 0),
            polarimetric_imaging=instruments_stats_count["rss_observing_mode_requested_total"].get("Polarimetric imaging", 0),
            spectropolarimetry=instruments_stats_count["rss_observing_mode_requested_total"].get("Spectropolarimetry", 0),
            spectroscopy=instruments_stats_count["rss_observing_mode_requested_total"].get("Spectroscopy", 0)
        ),

        salticam_detector_mode_total=DetectorMode(
            drift_scan=instruments_stats_count["scam_detector_mode_total"].get("DRIFTSCAN", 0),
            frame_transfer=instruments_stats_count["scam_detector_mode_total"].get("FRAME XFER", 0),
            normal=instruments_stats_count["scam_detector_mode_total"].get("NORMAL", 0),
            slot_mode=instruments_stats_count["scam_detector_mode_total"].get("SLOT", 0)
        ),
        salticam_detector_mode_requested_total=DetectorMode(
            drift_scan=instruments_stats_count["scam_detector_mode_requested_total"].get("DRIFTSCAN", 0),
            frame_transfer=instruments_stats_count["scam_detector_mode_requested_total"].get("FRAME XFER", 0),
            normal=instruments_stats_count["scam_detector_mode_requested_total"].get("NORMAL", 0),
            slot_mode=instruments_stats_count["scam_detector_mode_requested_total"].get("SLOT", 0)
        ),

        scam_total=instruments_stats_count["scam_total"],
        scam_requested_total=instruments_stats_count["scam_requested_total"]
    )


def targets(proposal_code_ids):
    """
    Basic target information that will be used for statistics.
    Like, RA and DEC of the target and if target P4

    :param proposal_code_ids: list
        List of proposal code ids
    :return: list[dict]
        The basic target information
    """
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


def observing_conditions(proposal_code_ids, partner, semester):
    """
    Get the statistics of observing conditions per seen and transparency, and fit it to schema.

    :param proposal_code_ids: list
        List of proposal code ids
    :param semester: str
        The semester
    :param partner: str
        The partner code
    :return: ObservingConditions
        The observing conditions
    """
    stats = transparency_and_seeing_statistics(proposal_code_ids, semester, partner)
    return ObservingConditions(
        transparency=TransparencyCondition(
            time_requested=stats["time_request_per_transparency"],
            number_of_proposals=stats["number_of_proposals_per_transparency"]
        ),
        seeing=SeeingCondition(
            time_requested=stats["time_request_per_seeing"],
            number_of_proposals=stats["number_of_proposals_per_seeing"]
        )
    )


def proposal_statistics(proposal_code_ids, semester):
    """
    Query and calculate proposals relate statistics

    :param proposal_code_ids: list
        List of proposal code ids
    :param semester: str
        The semester
    :return: dict
        Proposal statistics
    """
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

    for proposal_code, stats in proposals.items():
        if not any([s < semester for s in stats["semesters"]]):
            new_proposals += 1
            if len(stats["semesters"]) > 1:
                new_long_term_proposals += 1
        if len(stats["semesters"]) > 1:
            long_term_proposals += 1
        if stats["is_p4"]:
            p4_proposals += 1
        if stats["is_thesis"]:
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
        proposals=proposal_statistics(proposal_code_ids, semester),
        targets=targets(proposal_code_ids),
        time_breakdown=time_breakdown(semester)
    )
