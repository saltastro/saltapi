from graphene import Boolean, InputObjectType, Int, List, Mutation, String
from util.time_allocations import update_time_allocations

class TimeAllocationInput(InputObjectType):
    """
    A time allocation for a proposal and priority.
    """

    proposal_code = String(required=True,
                           description='The proposal code, such as \'2017-2-SCI-042\'.')
    priority = Int(required=True,
                   description='The priority as an integer between 0 and 4 (both inclusive).')
    time = Int(required=True,
               description='The allocated time for the proposal code and priority, in seconds.')


class TacCommentInput(InputObjectType):
    """
    A tac comment for a proposal
    """

    proposal_code = String(required=True,
                           description='The proposal code, such as \'2017-2-SCI-042\'.')
    comment = String(required=True,
                     description='The comment made by tac while they were allocating time.')


class TimeAllocationsInput(InputObjectType):
    """
    Time allocations for a partner and semester.
    """

    partner = String(required=True,
                     description='The partner code, such as \'RSA\' or \'IUCAA\'.')
    semester = String(required=True,
                      semester='The semester, such as \'2017-2\' or \'2018-1\'.')
    time_allocations = List(TimeAllocationInput,
                            required=True,
                            description='The time allocations.')
    tac_comments = List(TacCommentInput,
                        required=True,
                        description='The tac comments.')


class UpdateTimeAllocations(Mutation):
    class Arguments:
        time_allocations = TimeAllocationsInput(required=True)

    success = Boolean()

    def mutate(self, info, time_allocations):
        is_updated = update_time_allocations(
            partner=time_allocations['partner'],
            semester=time_allocations['semester'],
            time_allocations=time_allocations['time_allocations'],
            tac_comments=time_allocations['tac_comments']
                                             )
        return UpdateTimeAllocations(is_updated)
