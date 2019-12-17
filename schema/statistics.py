from graphene import Enum
from graphene import List
from graphene import ObjectType, String, Field, Float, Union


class Conditions(ObjectType):
    clear = Float()
    thick_cloud = Float()
    thin_cloud = Float()
    any = Float()


class StatisticsPartner(Enum):
    ALL = "All"
    RSA = "RSA"
    UW = "UW"


class ObservingConditions(ObjectType):
    time_requested = Field(Conditions)
    number_of_proposals = Field(Conditions)
    completion = Field(Conditions)


class Priorities(ObjectType):
    p0_p1 = Float()
    p2 = Float()
    p3 = Float()


class TimeBreakdown(ObjectType):
    engineering = Float()
    idle = Float()
    lost_to_problems = Float()
    lost_to_weather = Float()
    science = Float()


class TimeSummary(ObjectType):
    allocated = Field(Priorities)
    observed = Field(Priorities)


class CompletionStatistics(ObjectType):
    partner = Field(String())
    observing_conditions = Field(ObservingConditions)
    summary = Field(TimeSummary)


class InstrumentStatistics(ObjectType):
    name = String


class TargetStatistics(ObjectType):
    name = String


class Statistics(ObjectType):
    # completion = List(CompletionStatistics, description="The completion statistics per partner")
    # instruments = List(InstrumentStatistics)
    # target = List(TargetStatistics)
    time_breakdown = Field(TimeBreakdown)
