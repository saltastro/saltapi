from graphene import ObjectType, String, ID, Float, Field, Boolean


class Position(ObjectType):
    dec = Float()
    ra = Float()
    dec_dot = Float()
    ra_dot = Float()
    epoch = String()


class Magnitude(ObjectType):
    min_magnitude = Float()
    max_magnitude = Float()
    filter = String()  # from bandpass


class Target(ObjectType):
    id = ID()
    name = String()
    is_optional = Boolean()
    position = Field(Position)
    magnitude = Field(Magnitude)
