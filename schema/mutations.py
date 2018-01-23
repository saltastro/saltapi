import graphene
from schema.time_allocations import UpdateTimeAllocations
from schema.technical_review import UpdateTechComments, UpdateLiaisonAstronomer


class Mutations(graphene.ObjectType):
    update_time_allocations = UpdateTimeAllocations.Field()
    update_tech_comments = UpdateTechComments.Field()
    update_liaison_astronomer = UpdateLiaisonAstronomer.Field()
