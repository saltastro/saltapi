from data.targets import *
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import relay
import graphene


class ProposalTarget(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ProposalTargetModel

    ProposalCode_Id = P1ProposalTargetModel.ProposalCode_Id


class Target(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetModel


class TargetCoordinates(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetCoordinatesModel

    RaH = TargetCoordinatesModel.RaH
    RaM = TargetCoordinatesModel.RaM
    RaS = TargetCoordinatesModel.RaS
    DecD = TargetCoordinatesModel.DecD
    DecM = TargetCoordinatesModel.DecM
    DecS = TargetCoordinatesModel.DecS
    DecSign = TargetCoordinatesModel.DecSign
    ra = graphene.Float()
    dec = graphene.Float()

    def resolve_ra(self, args, context, info):
        return (int(self.RaH) + int(self.RaM) / 60 + float(self.RaS) / 3600) / (24 / 360)

    def resolve_dec(self, args, context, info):
        sign = -1 if self.DecSign == '-' else 1
        return sign * (float(self.DecD) + float(self.DecM) / 60 + float(self.DecS) / 3600)


class TargetMagnitudes(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetMagnitudesModel


class TargetSubType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetSubTypeModel


class Moon(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MoonModel


class PiRanking(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiRankingModel

targets_list = [ProposalTarget,
                Target,
                TargetCoordinates,
                TargetMagnitudes,
                TargetSubType,
                Moon,
                PiRanking
                ]
