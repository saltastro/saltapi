from graphene import ObjectType, String, ID, Boolean, Field, Int, List, Float
from schema.instruments import Instruments
from schema.target import Target


class Investigator(ObjectType):
    id = ID()
    first_name = String()
    surname = String()
    email = String()


class ProposalInfoM(ObjectType):
    is_p4 = Boolean()
    status = String()
    transparency = String()
    max_seeing = Float()


class PI(ObjectType):
    surname = String()
    name = String()
    email = String()


class Distribution(ObjectType):
    partner_name = String()
    partner_code = String()
    time = Int()


class RequestedTimeM(ObjectType):
    semester = String()
    distribution = Field(List(Distribution))
    minimum_useful_time = Int()


class ProposalAllocatedTime(ObjectType):
    partner_code = String()
    partner_name = String()
    p0 = Float()
    p1 = Float()
    p2 = Float()
    p3 = Float()
    p4 = Float()


class Proposals(ObjectType):
    id = ID()
    code = String()
    title = String()
    abstract = String()
    is_p4 = Boolean()
    status = String()
    transparency = String()
    max_seeing = Float()
    time_requests = List(RequestedTimeM)
    is_thesis = Boolean()
    instruments = Field(Instruments)
    targets = Field(List(Target))
    pi = Field(PI)
    tech_report = String()
    allocated_time = List(ProposalAllocatedTime)
