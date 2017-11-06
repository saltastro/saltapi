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

    proposals = graphene.List(Proposal, semester=graphene.String())
    targets = graphene.List(ProposalTarget, semester=graphene.String())
    instruments = graphene.List(P1Config, semester=graphene.String())
    user = graphene.Field(User, description="This is a wm user you would need to be having a on your header to query. ")

    def resolve_proposals(self, context, info, args):
        query = Proposal.get_query(info)
        ids = Proposal.get_proposal_ids(semester=context['semester'])
        results = query.filter(Proposal.Proposal_Id.in_(ids['ProposalIds'])).all()
        return results

    def resolve_targets(self, context, info, args):
        query = ProposalTarget.get_query(info)
        ids = Proposal.get_proposal_ids(semester=context['semester'])
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


schema = graphene.Schema(query=Query, types=list_to_map)
