from schema.proposals import Proposal
from schema.partner import *
from schema.selectors import Selectors
from schema.proposal_manual import *
from data.proposal_manual import get_proposals
from data.partner import get_partners
from data.selectors import get_selectors_data
from schema.targets import *
from schema.instruments import *
from schema.user import *
from schema.user import PiptUser as User
import graphene
from graphene import relay, Field, List, String

list_to_map = instruments_list + targets_list + user_list


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    proposals_m = Field(List(ProposalM), semester=String(), partner_code=String(), proposal_code=String())
    targets = graphene.List(ProposalTarget, semester=String(), partner_code=String(), proposal_code=String())
    instruments = graphene.List(P1Config, semester=String())
    user = graphene.Field(User, description="This is a wm user you would need to be having a on your header to query. ")
    partners_allocations = Field(List(PartnersAllocations), semester=String(), partner_code=String(),
                                 description="List of all allocations of SALT Partners")
    selectors = Field(Selectors)

    def resolve_targets(self, context, info, args, partner_code=None, proposal_code=None):
        query = ProposalTarget.get_query(info)
        if 'partner_code' in context:
            partner = context['partner_code']
        else:
            partner = partner_code

        if 'proposal_code' in context:
            proposal = context['proposal_code']
        else:
            proposal = proposal_code

        ids = Proposal.get_proposal_ids(semester=context['semester'], partner_code=partner, proposal_code=proposal)
        results = query.filter(ProposalTarget.ProposalCode_Id.in_(ids['ProposalCodeIds'])).all()

        return results

    def resolve_user(self, context, info , args):
        query =User.get_query(info)

        results = query.filter(User.username == "nhlavutelo").first()
        return results

    def resolve_proposals_m(self, context, info, args, partner_code=None, proposal_code=None):
        if 'partner_code' in context:
            partner = context['partner_code']
        else:
            partner = partner_code

        if 'proposal_code' in context:
            proposal = context['proposal_code']
        else:
            proposal = proposal_code

        return get_proposals(semester=context['semester'], partner_code=partner, proposal_code=proposal)

    def resolve_partners_allocations(self, context, info, args, partner_code=None, semester=None):
        if 'partner_code' in context:
            partner_code = context['partner_code']

        if 'semester' in context:
            semester = context['semester']

        return get_partners(semester=semester, partner_code=partner_code)

    def resolve_selectors(self, context, info, args):
        return get_selectors_data()


schema = graphene.Schema(query=Query, types=list_to_map)
