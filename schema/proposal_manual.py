from graphene import ObjectType, String, ID, Boolean, Field, Int, List, Float


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
    proposal_id = ID()
    proposal_code = String()
    general_info = Field(ProposalInfoM)
    requester_time = List(RequestedTimeM)
    total_time_requested = Int()
    is_new = Boolean()
