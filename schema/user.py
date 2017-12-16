from graphene import ObjectType, String, List, Field


class Role(ObjectType):
    type = String()
    partners = Field(List(String))


class UserModel(ObjectType):
    first_name = String()
    last_name = String()
    email = String()
    username = String()
    role = Field(List(Role))
