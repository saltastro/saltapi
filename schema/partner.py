from graphene import ObjectType, ID, Int, String, Float, List


class AllocatedTime(ObjectType):
    for_semester = String()

    Allocated_p0_p1 = Float()
    Allocated_p2 = Float()
    Allocated_p3 = Float()

    used_p0_p1 = Float()
    used_p2 = Float()
    used_p3 = Float()


class RequestedTime(ObjectType):
    p0 = Int()
    p1 = Int()
    p2 = Int()
    p3 = Int()
    p4 = Int()


class ScienceTime(ObjectType):
    p0 = Int()
    p1 = Int()
    p2 = Int()
    p3 = Int()
    p4 = Int()


class PartnersAllocations(ObjectType):
    id = ID()
    name = String()
    code = String()
    allocated_time = List(AllocatedTime)
    requested_time = List(RequestedTime)
    science_time = List(ScienceTime)
