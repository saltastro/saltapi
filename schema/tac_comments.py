from graphene import Boolean, InputObjectType, Int, List, Mutation, String
from util.tac_comments import update_tac_comments

class TacCommentInput(InputObjectType):
    """
    A tac comment for a proposal
    """

    proposal_code = String(required=True,
                           description='The proposal code, such as \'2017-2-SCI-042\'.')
    comment = String(required=True,
                     description='The comment made by tac while they were allocating time.')


class TacCommentsInput(InputObjectType):
    """
    Tac Comment for a partner and semester
    """

    partner = String(required=True,
                     description='The partner code, such as \'RSA\' or \'IUCAA\'.')
    semester = String(required=True,
                      semester='The semester, such as \'2017-2\' or \'2018-1\'.')
    tac_comments = List(TacCommentInput,
                         required=True,
                         description='The tac Comment.')


class UpdateTacComments(Mutation):
    class Arguments:
        tac_comments = TacCommentsInput(required=True)

    success = Boolean()

    def mutate(self, info, tac_comments):
        update_tac_comments(partner=tac_comments['partner'],
                            semester=tac_comments['semester'],
                            tac_comments=tac_comments['tac_comments'])
        return UpdateTacComments(True)
