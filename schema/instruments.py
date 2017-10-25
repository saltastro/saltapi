from data.instruments import *
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import relay

class P1Config(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ConfigModel

    ProposalCode_Id = P1ConfigModel.ProposalCode_Id

    def resolve_Proposal_Id(self, args, context, info):
        return "proposal: " + str(self.ProposalCode_Id)


class P1Hrs(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1HrsModel


class HrsMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsModeModel


class P1Bvit(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1BvitModel


class BvitFilter(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BvitFilterModel


class P1Salticam(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1SalticamModel


class SalticamDetectorMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamDetectorModeModel


class P1Rss(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssModel


class RssDetectorMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssDetectorModeModel


class RssMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssModeModel


class P1RssSpectroscopy(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssSpectroscopyModel


class RssGrating(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssGratingModel


class P1RssMask(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssMaskModel


class RssMaskType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssMaskTypeModel


class P1RssFabryPerot(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssFabryPerotModel


class RssFabryPerotMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssFabryPerotModeModel


class RssEtalonConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssEtalonConfigModel


class P1RssPolarimetry(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssPolarimetryModel


class RssPolarimetryPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssPolarimetryPatternModel



instruments_list = [
    P1Config,
    P1Hrs,
    HrsMode,
    P1Bvit,
    BvitFilter,
    P1Salticam,
    SalticamDetectorMode,
    P1Rss,
    RssDetectorMode,
    RssMode,
    P1RssSpectroscopy,
    RssGrating,
    P1RssMask,
    RssMaskType,
    P1RssFabryPerot,
    RssFabryPerotMode,
    RssEtalonConfig,
    P1RssPolarimetry,
    RssPolarimetryPattern
]