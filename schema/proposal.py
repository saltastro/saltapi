from graphene import ObjectType, String, ID, Boolean, Field, Int, List, Float
from schema.instruments import Instruments
from schema.salt_astronomer import SALTAstronomer
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


class TacComment(ObjectType):
    partner_code = String()
    comment = String()

    def __eq__(self, other):
        return self.partner_code == other.partner_code and self.comment == other.comment


class Proposals(ObjectType):
    abstract = String()
    allocated_time = List(ProposalAllocatedTime)
    code = String()
    id = ID()
    instruments = Field(Instruments)
    is_p4 = Boolean()
    is_thesis = Boolean()
    max_seeing = Float()
    pi = Field(PI)
    status = String()
    tac_comment = List(TacComment)
    targets = Field(List(Target))
    tech_report = String()
    time_requests = List(RequestedTimeM)
    title = String()
    transparency = String()
    S_a_l_t_astronomer = Field(SALTAstronomer)
    reviewer = Field(SALTAstronomer)
