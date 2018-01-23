from graphene import Boolean, InputObjectType, List, Mutation, String
from util.technical_review import update_tech_comments, update_liaison_astronomers


class TechCommentInput(InputObjectType):
    """
    A tech comment for a proposal
    """

    proposal_code = String(required=True,
                           description='The proposal code, such as \'2017-2-SCI-042\'.')

    comment = String(required=True,
                     description='The comment made by tac while they were allocating time.')


class TechCommentsInput(InputObjectType):
    """
    Time allocations for a partner and semester.
    """

    semester = String(required=True,
                      semester='The semester, such as \'2017-2\' or \'2018-1\'.')
    S_a_l_t_astronomer = String(required=True,
                                description='Salt Astronomer updating a comment username')
    tech_comments = List(TechCommentInput,
                         required=True,
                         description='The tech comments.')


class ProposalLiaisonInput(InputObjectType):
    """
    A tech comment for a proposal
    """

    liaison_astronomer = String(required=True,
                                description='Salt Astronomer being assigned')
    proposals = List(String,
                     required=True,
                     description='List of proposals to be assigned')


class ProposalsLiaisonInput(InputObjectType):
    """
    Time allocations for a partner and semester.
    """

    semester = String(required=True,
                      semester='The semester, such as \'2017-2\' or \'2018-1\'.')
    proposals_assigned = List(ProposalLiaisonInput,
                              required=True,
                              description='A list of (SA and list of proposal codes to SA) ')


class UpdateTechComments(Mutation):
    class Arguments:
        tech_comments = TechCommentsInput(required=True)

    success = Boolean()

    def mutate(self, info, tech_comments):
        is_updated = update_tech_comments(
            semester=tech_comments['semester'],
            S_a_l_t_astronomer=tech_comments['S_a_l_t_astronomer'],
            tech_comments=tech_comments['tech_comments']
                                             )
        return UpdateTechComments(is_updated)


class UpdateLiaisonAstronomer(Mutation):
    class Arguments:
        proposals_liaison = ProposalsLiaisonInput(required=True)

    success = Boolean()

    def mutate(self, info, proposals_liaison):
        is_updated = update_liaison_astronomers(
            semester=proposals_liaison['semester'],
            proposals_assigned=proposals_liaison['proposals_assigned']
                                             )
        return UpdateLiaisonAstronomer(is_updated)
