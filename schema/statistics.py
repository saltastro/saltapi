from graphene import Boolean
from graphene import Enum
from graphene import List
from graphene import ObjectType, String, Field, Float, Union


class CloudConditions(ObjectType):
    any = Float()
    clear = Float()
    thick_cloud = Float()
    thin_cloud = Float()


class SeeingConditions(ObjectType):
    less_equal_1_dot_5 = Float()
    less_equal_2 = Float()
    less_equal_3 = Float()
    more_than_3 = Float()


class StatisticsPartner(Enum):
    ALL = "ALL"
    AMNH = "AMNH"
    DC = "DC"
    IUCAA = "IUCAA"
    POL = "POL"
    RSA = "RSA"
    RU = "RU"
    UKSC = "UKSC"
    UNC = "UNC"
    UW = "UW"


class SeeingCondition(ObjectType):
    time_requested = Field(SeeingConditions)
    number_of_proposals = Field(SeeingConditions)


class CloudCondition(ObjectType):
    time_requested = Field(CloudConditions)
    number_of_proposals = Field(CloudConditions)


class ObservingConditions(ObjectType):
    clouds = Field(CloudCondition)
    seeing = Field(SeeingCondition)


class Priorities(ObjectType):
    p0 = Float()
    p1 = Float()
    p2 = Float()
    p3 = Float()
    p4 = Float()


class TimeBreakdown(ObjectType):
    engineering = Float()
    idle = Float()
    lost_to_problems = Float()
    lost_to_weather = Float()
    science = Float()


class TimeSummary(ObjectType):
    allocated_time = Field(Priorities)
    observed_time = Field(Priorities)


class CompletionStatistics(ObjectType):
    partner = Field(StatisticsPartner)
    summary = Field(TimeSummary)
    share_percentage = Float()


class Instruments(ObjectType):
    bvit = Float()
    hrs = Float()
    salticam = Float()
    rss = Float()


class ExposureMode(ObjectType):
    low_resolution = Float()
    medium_resolution = Float()
    high_resolution = Float()
    high_stability = Float()
    int_cal_fibre = Float()


class ObservingMode(ObjectType):
    fabry_perot = Float()
    fabry_perot_polarimetry = Float()
    mos = Float()
    mos_polarimetry = Float()
    imaging = Float()
    polarimetric_imaging = Float()
    spectropolarimetry = Float()
    spectroscopy = Float()


class DetectorMode(ObjectType):
    drift_scan = Float()
    frame_transfer = Float()
    normal = Float()
    shuffle = Float()
    slot_mode = Float()


class InstrumentStatistics(ObjectType):
    time_requested_per_instrument = Field(Instruments)
    number_of_configurations_per_instrument = Field(Instruments)
    time_requested_per_rss_detector = Field(DetectorMode)
    number_of_configurations_per_rss_detector = Field(DetectorMode)
    time_requested_per_salticam_detector = Field(DetectorMode)
    number_of_configurations_per_salticam_detector = Field(DetectorMode)
    time_requested_per_hrs_exposure = Field(ExposureMode)
    number_of_configurations_per_hrs_exposure = Field(ExposureMode)
    time_requested_per_rss_observing_mode = Field(ObservingMode)
    number_of_configurations_per_rss_observing_mode = Field(ObservingMode)


class StatisticsTarget(ObjectType):
    is_optional = Boolean()
    right_ascension = Float()
    declination = Float()


class ProposalStatistics(ObjectType):
    number_of_proposals = Float()
    new_proposals = Float()
    long_term_proposals = Float()
    new_long_term_proposals = Float()
    thesis_proposals = Float()
    p4_proposals = Float()


class Statistics(ObjectType):
    completion = List(CompletionStatistics, description="The completion statistics per partner")
    instruments = Field(InstrumentStatistics)
    observing_conditions = Field(ObservingConditions)
    proposal_statistics = Field(ProposalStatistics)
    targets = List(StatisticsTarget)
    time_breakdown = Field(TimeBreakdown)
