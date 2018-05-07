from graphene import ObjectType, String, ID, Float, Field, Boolean


class Coordinates(ObjectType):
    dec = Float()
    ra = Float()


class Moving(ObjectType):
    dec_dot = Float()
    ra_dot = Float()
    epoch = String()


class Magnitudes(ObjectType):
    minimum = Float()
    maximum = Float()
    filter_name = String()  # from bandpass


class Target(ObjectType):
    id = ID()
    name = String()
    optional = Boolean()
    coordinates = Field(Coordinates)
    magnitudes = Field(Magnitudes)
    moving = Field(Moving)
