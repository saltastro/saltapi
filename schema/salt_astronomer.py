from graphene import ObjectType, String


class SALTAstronomer(ObjectType):
    name = String()
    surname = String()
    email = String()
    username = String()
