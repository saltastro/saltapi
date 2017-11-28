from flask import g
from graphene import ObjectType, String, ID, Boolean, Field, Int, List, Float, resolve_only_args
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


class TimePerPartner(ObjectType):
    partner_name = String()
    partner_code = String()
    time = String()


class RequestedTimeM(ObjectType):
    for_semester = String()
    moon = String()
    total_time = Int()
    time_per_partner = Field(List(TimePerPartner))


class Proposals(ObjectType):
    id = ID()
    code = String()
    title = String()
    abstract = String()
    semester = String()
    general_info = Field(ProposalInfoM)
    time_requests = List(RequestedTimeM)
    total_time_requested = Int()
    minimum_useful_time = Int()
    is_thesis = Boolean()
    instruments = Field(Instruments)
    targets = Field(List(Target))
    pi = Field(PI)
    tech_report = String()

