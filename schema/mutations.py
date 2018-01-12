import graphene
from schema.time_allocations import UpdateTimeAllocations
from schema.tac_comments import UpdateTacComments


class Mutations(graphene.ObjectType):
    update_time_allocations = UpdateTimeAllocations.Field()
    update_tac_comments = UpdateTacComments.Field()
