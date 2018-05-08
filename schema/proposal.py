from graphene import ObjectType, String, Boolean, Field, Int, List, Float
from schema.instruments import Instruments
from schema.partner import Partner
from schema.target import Target
from schema.user import User


class ProposalInfoM(ObjectType):
    is_p4 = Boolean()
    status = String()
    transparency = String()
    max_seeing = Float()


class PartnerTimeRequest(ObjectType):
    partner = Field(Partner)
    time = Int()


class TimeRequest(ObjectType):
    semester = String()
    partnerTimeRequest = Field(List(PartnerTimeRequest))
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
        return self.partner_code == other.partner_code and self.comment == other.comment


class TechReview(ObjectType):
    semester = String()
    reviewer = Field(User)
    report = String()


class Proposals(ObjectType):
    abstract = String()
    is_target_of_opportunity = Boolean()
    allocated_time = List(ProposalAllocatedTime)
    code = String()
    instruments = Field(Instruments)
    is_p4 = Boolean()
    is_thesis = Boolean()
    max_seeing = Float()
    principal_investigator = Field(User)
    principal_contact = Field(User)
    status = String()
    tac_comment = List(TacComment)
    targets = Field(List(Target))
    tech_reviews = Field(List(TechReview))
    time_requests = List(TimeRequest)
    title = String()
    transparency = String()
    liaison_salt_astronomer = Field(User)
