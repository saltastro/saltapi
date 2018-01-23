import graphene
from schema.time_allocations import UpdateTimeAllocations


class Mutations(graphene.ObjectType):
    update_time_allocations = UpdateTimeAllocations.Field()
