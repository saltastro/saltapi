from graphene import ObjectType, Interface, String, Field


class Instrument(Interface):
    type = String()


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
    class Meta:
        interfaces = (Instrument,)
    filter = String()


class SCAM(ObjectType):
    class Meta:
        interfaces = (Instrument,)
    detector_mode = String()


class HRS(ObjectType):
    class Meta:
        interfaces = (Instrument,)
    detector_mode = String()


class RSS(ObjectType):
    class Meta:
        interfaces = (Instrument,)
    mode = String()
    detector_mode = String()
    spectroscopy = Field(Spectroscopy)
    fabry_perot = Field(FabryPerot)
    polarimetry = Field(Polarimetry)
    mask = Field(Mask)
