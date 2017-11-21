from graphene import ObjectType, String, ID, Boolean, Field, Int, List, Float


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


class RequestedTimeM(ObjectType):
    for_semester = String()
    moon = String()
    time = Int()


class ProposalM(ObjectType):
    id = ID()
    code = String()
    general_info = Field(ProposalInfoM)
    requester_time = List(RequestedTimeM)
    total_time_requested = Int()
    minimum_useful_time = Int()
    is_thesis = Boolean()
