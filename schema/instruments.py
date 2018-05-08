from graphene import ObjectType, String, List, Field


class Spectroscopy(ObjectType):
    grating = String()


class Polarimetry(ObjectType):
    waveplate_pattern = String()


class FabryPerot(ObjectType):
    mode = String()
    description = String()
    etalon_config = String()


class Mask(ObjectType):
    type = String()
    mos_description = String()


class BVIT(ObjectType):
    type = String()
    filter = String()


class SCAM(ObjectType):
    type = String()
    detector_mode = String()
    xml_detector_mode = String()


class HRS(ObjectType):
    detector_mode = String()
    type = String()


class RSS(ObjectType):
    type = String()
    mode = String()
    detector_mode = String()
    xml_detector_mode = String()
    spectroscopy = Field(Spectroscopy)
    fabry_perot = Field(FabryPerot)
    polarimetry = Field(Polarimetry)
    mask = Field(Mask)


class Instruments(ObjectType):
    rss = List(RSS)
    hrs = List(HRS)
    bvit = List(BVIT)
    scam = List(SCAM)
