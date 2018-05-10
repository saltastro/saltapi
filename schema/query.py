import graphene
from flask import g
from schema.partner import *
from schema.proposal import *
from data.user import get_salt_users, get_tac_members
from data.proposal import get_proposals
from data.partner import get_partners
from data.targets import get_targets
from data.salt_astronomer import get_salt_astronomer
from schema.instruments import HRS, RSS, BVIT, SCAM
from schema.user import User, TacMember
from schema.mutations import Mutations


class Query(graphene.ObjectType):
    proposals = Field(List(Proposal), semester=String(), partner_code=String(),
                      description="List of proposals per semester. Can be reduced to per partner "
                                  "Semester must be provided to reduce query load")
    public_proposals = Field(List(Proposal), semester=String(), partner_code=String(),
                             description="List of proposals per semester. Can be reduced to per partner "
                                         "Semester must be provided to reduce query load. These proposal only provide "
                                         "information which is not critical to the proposal (best to use for SALT"
                                         " statistics)")
    targets = Field(List(Target), semester=String(), partner_code=String(), proposal_code=String(),
                    description="List of targets per semester can be reduced to per partner or per proposal. " 
                                " Semester must be provided in all cases")
    partner_allocations = Field(List(Partner), semester=String(), partner_code=String(),
                                description="List of all allocations of SALT Partners")
    user = Field(User)
    salt_astronomers = Field(List(User))
    tac_members = Field(List(TacMember), partner_code=String())
    salt_users = Field(List(User), partner_code=String())

    def resolve_proposals(self, info, semester=None, partner_code=None):
        if semester is None:
            raise ValueError("please provide argument \"semester\"")
        return get_proposals(semester=semester, partner_code=partner_code)

    def resolve_public_proposals(self, info, semester=None, partner_code=None):
        if semester is None:
            raise ValueError("please provide argument \"semester\"")
        return get_proposals(semester=semester, partner_code=partner_code)

    def resolve_targets(self, info, semester=None, partner_code=None,):
        if semester is None:
            raise ValueError("please provide argument \"semester\"")
        return get_targets(semester=semester, partner_code=partner_code)

    def resolve_partner_allocations(self, info, semester=None, partner_code=None):
        if semester is None:
            raise ValueError("please provide argument \"semester\"")
        return get_partners(semester=semester, partner=partner_code)

    def resolve_user(self, info):
        return g.user

    def resolve_salt_astronomers(self, info):
        return get_salt_astronomer()

    def resolve_tac_members(self, info, partner_code=None):
        return get_tac_members(partner_code)

    def resolve_salt_users(self, info):
        return get_salt_users()


schema = graphene.Schema(query=Query, mutation=Mutations, types=[HRS, RSS, BVIT, SCAM])
