from graphene import ObjectType, String, ID, Float, Field


class Coordinates(ObjectType):
    dec = Float()
    ra = Float()


class Horizon(ObjectType):
    dec = Float()
    ra = Float()


class Magnitudes(ObjectType):
    minimum = Float()
    maximum = Float()
    filter_name = String()  # from bandpass


class Target(ObjectType):
    id = ID()
    name = String()
    coordinates = Field(Coordinates)
    magnitudes = Field(Magnitudes)
