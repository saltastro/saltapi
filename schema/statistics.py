from graphene import Boolean
from graphene import Enum
from graphene import List
from graphene import ObjectType, Field, Float, Int


class TransparencyTimeDistribution(ObjectType):
    """
    Types of transparencies that SALT supports
    """
    any = Float()
    clear = Float()
    thick_cloud = Float()
    thin_cloud = Float()


class TransparencyNumberDistribution(ObjectType):
    """
    Types of transparencies that SALT supports
    """
    any = Int()
    clear = Int()
    thick_cloud = Int()
    thin_cloud = Int()


class SeeingTimeDistribution(ObjectType):
    """
    Distribution of time from the maximum seeing request per category.
    "less_equal_1_dot_5" means seeing between 0 and 1.5 arcseconds, "less_equal_2" means it is between 1.5 and 2
    arcseconds, and so forth
    """
    less_equal_1_dot_5 = Float()
    less_equal_2 = Float()
    less_equal_2_dot_5 = Float()
    less_equal_3 = Float()
    more_than_3 = Float()


class SeeingNumberDistribution(ObjectType):
    """
    Number of proposals requesting time from the maximum seeing request per category.
    "less_equal_1_dot_5" means seeing between 0 and 1.5 arcseconds, "less_equal_2" means it is between 1.5 and 2
    arcseconds, and so forth
    """
    less_equal_1_dot_5 = Int()
    less_equal_2 = Int()
    less_equal_2_dot_5 = Int()
    less_equal_3 = Int()
    more_than_3 = Int()


class StatisticsPartner(Enum):
    """
    SALT partner code
    """
    ALL = "ALL"
    AMNH = "AMNH"
    DC = "DC"
    DUR = "DUR"
    GU = "GU"
    IUCAA = "IUCAA"
    POL = "POL"
    RSA = "RSA"
    RU = "RU"
    UC = "UC"
    UKSC = "UKSC"
    UNC = "UNC"
    UW = "UW"


class SeeingCondition(ObjectType):
    """
    The seeing observing condition
    """
    time_requested = Field(SeeingTimeDistribution)
    number_of_proposals = Field(SeeingNumberDistribution)


class TransparencyCondition(ObjectType):
    """
    The transparency observing condition
    """
    time_requested = Field(TransparencyTimeDistribution)
    number_of_proposals = Field(TransparencyNumberDistribution)


class ObservingConditions(ObjectType):
    """
    The observing condition statistics per seeing and transparency
    """
    transparency = Field(TransparencyCondition)
    seeing = Field(SeeingCondition)


class Priorities(ObjectType):
    """
    The SALT observing and allocating priorities
    """
    p0 = Float()
    p1 = Float()
    p2 = Float()
    p3 = Float()
    p4 = Float()


class TimeBreakdown(ObjectType):
    """
    The time breakdown
    """
    engineering = Float()
    idle = Float()
    lost_to_problems = Float()
    lost_to_weather = Float()
    science = Float()


class TimeSummary(ObjectType):
    """
    the Time summary
    """
    allocated_time = Field(Priorities)
    observed_time = Field(Priorities)


class CompletionStatistics(ObjectType):
    """
    The observed completion statistics of a partner
    """
    partner = Field(StatisticsPartner)
    summary = Field(TimeSummary)
    share_percentage = Float()


class Instruments(ObjectType):
    """
    SALT instruments
    """
    bvit = Float()
    hrs = Float()
    salticam = Float()
    rss = Float()


class Resolution(ObjectType):
    """
    The HRS exposure mode
    """
    low_resolution = Float()
    medium_resolution = Float()
    high_resolution = Float()
    high_stability = Float()
    int_cal_fibre = Float()


class ObservingMode(ObjectType):
    """
    The observing mode for some of salt instruments
    """
    fabry_perot = Float()
    fabry_perot_polarimetry = Float()
    mos = Float()
    mos_polarimetry = Float()
    imaging = Float()
    polarimetric_imaging = Float()
    spectropolarimetry = Float()
    spectroscopy = Float()


class DetectorMode(ObjectType):
    """
    The detector mode for some of salt instruments
    """
    drift_scan = Float()
    frame_transfer = Float()
    normal = Float()
    shuffle = Float()
    slot_mode = Float()


class InstrumentStatistics(ObjectType):
    """
    The statistics related to SALT instruments
    """

    bvit_total = Float()
    bvit_requested_total = Float()

    hrs_total = Float()
    hrs_requested_total = Float()

    hrs_resolution_total = Field(Resolution)
    hrs_resolution_requested_total = Field(Resolution)

    rss_total = Float()
    rss_requested_total = Float()

    rss_detector_mode_total = Field(DetectorMode)
    rss_detector_mode_requested_total = Field(DetectorMode)

    rss_observing_mode_total = Field(ObservingMode)
    rss_observing_mode_requested_total = Field(ObservingMode)

    salticam_detector_mode_total = Field(DetectorMode)
    salticam_detector_mode_requested_total = Field(DetectorMode)

    scam_total = Float()
    scam_requested_total = Float()


class StatisticsTarget(ObjectType):
    """
    The statistics related to SALT targets
    """
    is_optional = Boolean()
    right_ascension = Float()
    declination = Float()


class ProposalStatistics(ObjectType):
    """
    The statistics related to SALT proposals
    """
    number_of_proposals = Float()
    new_proposals = Float()
    long_term_proposals = Float()
    new_long_term_proposals = Float()
    thesis_proposals = Float()
    p4_proposals = Float()


class Statistics(ObjectType):
    """
    The statistics data for SALT
    """
    completion = List(CompletionStatistics, description="The completion statistics per partner")
    instruments = Field(InstrumentStatistics)
    observing_conditions = Field(ObservingConditions)
    proposals = Field(ProposalStatistics)
    targets = List(StatisticsTarget)
    time_breakdown = Field(TimeBreakdown)
