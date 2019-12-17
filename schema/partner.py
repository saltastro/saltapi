from graphene import ObjectType, ID, String, Float,  Field, Enum


class Priority(ObjectType):
    p0_andp1 = Float()
    p2 = Float()
    p3 = Float()
    p4 = Float()


class TimeAllocation(ObjectType):
    semester = String()
    used_time = Field(Priority)
    allocated_time = Field(Priority)
    science_time = Field(Priority)


class Partner(ObjectType):
    id = ID()
    name = String()
    code = String()
    time_allocation = Field(TimeAllocation)


class PartnerGroupType(Enum):
    ALL = "All"


class PartnerGroup(ObjectType):
    group_type = PartnerGroupType()
