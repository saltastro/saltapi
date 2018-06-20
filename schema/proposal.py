from graphene import ObjectType, String, Boolean, Field, Int, List, Float
from graphene import resolve_only_args

from schema.instruments import Instrument, HRS, RSS
from schema.partner import Partner
from schema.target import Target
from schema.user import User


class ProposalInfo(ObjectType):
    is_p4 = Boolean()
    status = String()
    transparency = String()
    max_seeing = Float()


class TimeRequest(ObjectType):
    partner = Field(Partner)
    time = Int()


class TimeRequirement(ObjectType):
    semester = String()
    time_requests = List(TimeRequest)
    minimum_useful_time = Int()


class ProposalAllocatedTime(ObjectType):
    partner = Field(Partner)
    p0 = Float()
    p1 = Float()
    p2 = Float()
    p3 = Float()
    p4 = Float()


class TacComment(ObjectType):
    partner = Field(Partner)
    comment = String()

    def __eq__(self, other):
        return self.partner.code == other.partner.code and self.comment == other.comment


class TechReview(ObjectType):
    semester = String()
    reviewer = Field(User)
    report = String()


class Proposal(ObjectType):
    abstract = String()
    is_target_of_opportunity = Boolean()
    allocated_times = List(ProposalAllocatedTime)
    code = String()
    is_p4 = Boolean()
    is_thesis = Boolean()
    max_seeing = Float()
    principal_investigator = Field(User)
    principal_contact = Field(User)
    status = String()
    tac_comments = List(TacComment)
    targets = Field(List(Target))
    tech_reviews = Field(List(TechReview))
    time_requirements = List(TimeRequirement)
    title = String()
    transparency = String()
    liaison_salt_astronomer = Field(User)
    instruments = List(Instrument)
