from schema.proposals import *
from schema.targets import *
from schema.instruments import *
from schema.user import *
from schema.user import PiptUser as User
import graphene
from graphene import relay

list_to_map = instruments_list + proposals_list + targets_list + user_list


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    proposals = graphene.List(Proposal, semester=graphene.String(), partner_code=graphene.String(), proposal_code=graphene.String())
    targets = graphene.List(ProposalTarget, semester=graphene.String(), partner_code=graphene.String(), proposal_code=graphene.String())
    instruments = graphene.List(P1Config, semester=graphene.String())
    user = graphene.Field(User, description="This is a wm user you would need to be having a on your header to query. ")
    semesters = graphene.List(Semester, description="List of simesters available on the SDB")
    partners = graphene.List(Partner, description="List od SALT Partners")

    def resolve_proposals(self, context, info, args, partner_code=None, proposal_code=None):
        query = Proposal.get_query(info)
        if 'partner_code' in context:
            partner = context['partner_code']
        else:
            partner = partner_code

        if 'proposal_code' in context:
            proposal = context['proposal_code']
        else:
            proposal = proposal_code

        ids = Proposal.get_proposal_ids(partner_code=partner, semester=context['semester'], proposal_code=proposal)
        results = query.filter(Proposal.proposal_id.in_(ids['ProposalIds'])).all()
        return results

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

    def resolve_instruments(self, context, info, args):
        query = P1Config.get_query(info)
        ids = Proposal.get_proposal_ids(semester=context['semester'])

        results = query.filter(P1Config.ProposalCode_Id.in_(ids['ProposalCodeIds'])).all()
        return results

    def resolve_user(self, context, info , args):
        query =User.get_query(info)

        results = query.filter(User.username == "nhlavutelo").first()
        return results

    def resolve_semesters(self, context, info, args):
        query = Semester.get_query(info)
        return query.all()
    def resolve_partners(self, context, info, args):
        query = Partner.get_query(info)
        return query.all()


schema = graphene.Schema(query=Query, types=list_to_map)
