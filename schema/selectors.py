from graphene import ObjectType, List, String


class Selectors(ObjectType):
    semester = List(String)
    partner = List(String)
