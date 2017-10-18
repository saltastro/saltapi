from data.all_sdb_tables import *
from graphene_sqlalchemy import SQLAlchemyObjectType
from data.common import Semester as TypeSemester, conn
import pandas as pd
from graphene import relay
import graphene

class ArcBible(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ArcBibleModel


class ArcExposure(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ArcExposureModel

#
# class AvailableDitherPatterns(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = AvailableDitherPatternsModel


class Bandpass(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BandpassModel


class BlindOffset(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlindOffsetModel


class Block(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockModel


class BlockChange(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockChangeModel


class BlockCode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockCodeModel

#
# class BlockPointWindow(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = BlockPointWindowModel


class BlockPool(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockPoolModel

#
# class BlockProbabilities(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = BlockProbabilitiesModel


class BlockRejectedReason(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockRejectedReasonModel

#
# class BlockScore(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = BlockScoreModel
#
#
# class BlockScoreTonight(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = BlockScoreTonightModel


class BlockStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockStatusModel


class BlockType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockTypeModel
#
#
# class BlockVisibilityWindow(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = BlockVisibilityWindowModel
#
#
# class BlockVisibilityWindow_AnyMoon(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = BlockVisibilityWindow_AnyMoonModel


class BlockVisibilityWindowType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockVisibilityWindowTypeModel


class BlockVisit(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockVisitModel


class BlockVisitStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BlockVisitStatusModel

#
# class BlockWeights(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = BlockWeightsModel


class ButtonClass(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ButtonClassModel


class Bvit(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BvitModel


class BvitFilter(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BvitFilterModel


class BvitMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BvitModeModel


class BvitNeutralDensity(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BvitNeutralDensityModel


class BvitPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BvitPatternModel


class BvitPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = BvitPatternDetailModel


class CalFilter(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = CalFilterModel


class CalibrationType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = CalibrationTypeModel


class Commissioning(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = CommissioningModel


class Concam(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ConcamModel


class DatabaseVersion(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DatabaseVersionModel


class Dimm(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DimmModel


class DitherPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DitherPatternModel


class DQ_FlatfieldAmpEdge(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DQ_FlatfieldAmpEdgeModel


class DQ_HrsArc(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DQ_HrsArcModel


class DQ_HrsOrder(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DQ_HrsOrderModel


class DQ_RssArcIntensity(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DQ_RssArcIntensityModel


class DQ_RssGain(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DQ_RssGainModel


class DQ_SalticamGain(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = DQ_SalticamGainModel


class EventSource(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = EventSourceModel


class EventType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = EventTypeModel


class Fault(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultModel


class FaultComment(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultCommentModel

#
# class FaultCommentDiff(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = FaultCommentDiffModel

#
# class FaultDiff(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = FaultDiffModel


class FaultRevision(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultRevisionModel


class FaultSeverity(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultSeverityModel


class FaultStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultStatusModel


class FaultSystemUser(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultSystemUserModel

#
# class FaultTag(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = FaultTagModel


class FaultType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultTypeModel


class FaultTypeTag(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FaultTypeTagModel


class FileData(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FileDataModel


class FindingChart(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FindingChartModel


class FitsHeaderHrs(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FitsHeaderHrsModel


class FitsHeaderImage(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FitsHeaderImageModel


class FitsHeaderPipeline(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FitsHeaderPipelineModel


class FitsHeaderRss(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FitsHeaderRssModel


class FitsHeaderSalticam(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = FitsHeaderSalticamModel


# class FixSoLogEvent(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = FixSoLogEventModel


class GuideMethod(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = GuideMethodModel


class GuideStar(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = GuideStarModel


class Handover(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HandoverModel


class HandoverStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HandoverStatusModel


class HorizonsTarget(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HorizonsTargetModel


class Hrs(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsModel


class HrsBlueDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsBlueDetectorModel


class HrsCalibrationType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsCalibrationTypeModel


class HrsConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsConfigModel


class HrsExposurePattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsExposurePatternModel


class HrsExposurePatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsExposurePatternDetailModel


class HrsExposureType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsExposureTypeModel


class HrsIodineCellPosition(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsIodineCellPositionModel


class HrsMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsModeModel


class HrsNightlyCalibration(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsNightlyCalibrationModel


class HrsNodAndShuffle(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsNodAndShuffleModel


class HrsPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsPatternModel


class HrsPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsPatternDetailModel


class HrsProcedure(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsProcedureModel


class HrsRedDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsRedDetectorModel


class HrsRoAmplifiers(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsRoAmplifiersModel


class HrsRoSpeed(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsRoSpeedModel


class HrsTargetLocation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = HrsTargetLocationModel


class Institute(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = InstituteModel


class InstituteName(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = InstituteNameModel


class Investigator(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = InvestigatorModel


class Lamp(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = LampModel


class MassDimm(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MassDimmModel


class MirrorAlignmentEvent(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MirrorAlignmentEventModel


class Moon(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MoonModel


class MovingGuideStar(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MovingGuideStarModel


class MovingTable(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MovingTableModel


class MovingTableFile(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MovingTableFileModel


class MovingTarget(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MovingTargetModel


class MultiPartner(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = MultiPartnerModel


class NightInfo(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = NightInfoModel


class NightLogs(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = NightLogsModel


class NightlogSingleSection(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = NightlogSingleSectionModel


# class ObjectAvailability(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = ObjectAvailabilityModel


class ObsConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ObsConfigModel


class Observation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ObservationModel


class ObservingWindow(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ObservingWindowModel


class ObsLogTable(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ObsLogTableModel


class OcsHrsBlueDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsHrsBlueDetectorModel


class OcsHrsBlueExposurePattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsHrsBlueExposurePatternModel


class OcsHrsConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsHrsConfigModel


class OcsHrsProcedure(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsHrsProcedureModel


class OcsHrsRedDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsHrsRedDetectorModel


class OcsHrsRedExposurePattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsHrsRedExposurePatternModel


class OcsPayloadConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsPayloadConfigModel


class OcsRssConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsRssConfigModel


class OcsRssDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsRssDetectorModel


class OcsRssDetectorWindow(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsRssDetectorWindowModel


class OcsRssEtalonPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsRssEtalonPatternModel


class OcsRssFocusPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsRssFocusPatternModel


class OcsRssHwPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsRssHwPatternModel

#
# class OcsRssMosReferenceStar(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = OcsRssMosReferenceStarModel


class OcsSalticamDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsSalticamDetectorModel


class OcsRssQwPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsRssQwPatternModel


class OcsSalticamConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsSalticamConfigModel


class OcsSalticamDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsSalticamDetectorModel


class OcsSalticamProcedure(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsSalticamProcedureModel


class OcsSalticamProcedurePattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsSalticamProcedurePatternModel


class OcsSalticamWindow(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsSalticamWindowModel


class OcsStep(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsStepModel


class OcsTargetInformation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsTargetInformationModel


class OcsTelescopeConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = OcsTelescopeConfigModel


class P1Bvit(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1BvitModel


class P1BvitSimulation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1BvitSimulationModel


class P1Config(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ConfigModel

#
# class P1ExternalFunding(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = P1ExternalFundingModel


class P1Hrs(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1HrsModel


class P1HrsSimulation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1HrsSimulationModel


class P1MinTime(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1MinTimeModel


class P1ObservingConditions(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ObservingConditionsModel


class P1ObservingWindow(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ObservingWindowModel


class P1OptionalTargets(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1OptionalTargetsModel


class P1P2Diff(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1P2DiffModel


class P1P2DiffType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1P2DiffTypeModel


class P1PreviousProposalStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1PreviousProposalStatusModel


class P1ProposalTarget(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ProposalTargetModel


class P1RequestedTime(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RequestedTimeModel


class P1Rss(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssModel


class P1RssFabryPerot(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssFabryPerotModel


class P1RssMask(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssMaskModel


class P1RssPolarimetry(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssPolarimetryModel


class P1RssSimulation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssSimulationModel


class P1RssSpectroscopy(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1RssSpectroscopyModel


class P1Salticam(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1SalticamModel


class P1SalticamFilterPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1SalticamFilterPatternModel


class P1SalticamFilterPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1SalticamFilterPatternDetailModel


class P1SalticamSimulation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1SalticamSimulationModel

#
# class P1TargetProbabilities(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = P1TargetProbabilitiesModel


class P1Thesis(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ThesisModel


class P1ToO(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = P1ToOModel


class Partner(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PartnerModel


class PartnerShareTimeDist(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PartnerShareTimeDistModel


class PayloadConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PayloadConfigModel


class PayloadConfigType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PayloadConfigTypeModel


class PeriodicTarget(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PeriodicTargetModel


class PeriodTimeDist(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PeriodTimeDistModel

#
# class PetriTemp(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = PetriTempModel


class PhaseConstraint(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PhaseConstraintModel


class PipelineConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PipelineConfigModel


class PipelineDataAccessMethod(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PipelineDataAccessMethodModel

#
# class PipelineDataQuality_CCD(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = PipelineDataQuality_CCDModel


class PipelineDocFormat(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PipelineDocFormatModel


class PipelineProposalStatistics(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PipelineProposalStatisticsModel


class PipelineStatistics(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PipelineStatisticsModel


class PipelineStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PipelineStatusModel


class PiptAsyncProposalCode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptAsyncProposalCodeModel


class PiptDisplayMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptDisplayModeModel


class PiptDisplayModeType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptDisplayModeTypeModel


class PiptEmailValidation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptEmailValidationModel


class PiptErrorLog(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptErrorLogModel


class PiptMailQueue(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptMailQueueModel


class PiptNews(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptNewsModel


class PiptSaltTAC(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptSaltTACModel


class PiptSavedQuery(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptSavedQueryModel


class PiptSetting(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptSettingModel


class PiptUser(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptUserModel


class PiptUserSetting(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptUserSettingModel


class PiptUserTAC(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptUserTACModel


class PiptVersions(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiptVersionsModel


class PiRanking(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PiRankingModel


class PointEvent(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PointEventModel


class Pointing(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PointingModel


class Pool(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PoolModel


class PoolAssignedTime(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PoolAssignedTimeModel


class PoolRule(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PoolRuleModel


# class PoolRuleSet(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = PoolRuleSetModel


class PriorityAlloc(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PriorityAllocModel


class Proposal(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalModel
    Proposal_Id = ProposalModel.Proposal_Id

    def resolve_Proposal_Id(self, args, context, info):
        return "proposal: " + str(self.Proposal_Id)

    @staticmethod
    def get_proposal_ids(**args):
        sql = " SELECT MAX(p.Proposal_Id) as Ids, Proposal_Code " \
              "  FROM Proposal AS p " \
              "    JOIN ProposalCode AS pc ON (p.ProposalCode_Id=pc.ProposalCode_Id) " \
              "    JOIN MultiPartner AS mp ON (mp.Proposal_Id=p.Proposal_Id) " \
              "    JOIN Partner AS pa ON (mp.Partner_Id=pa.Partner_Id) " \
              "  WHERE Phase=1 "
        if 'semester' in args:
            semester = TypeSemester.get_semester(semester_code=args['semester'])
            sql = sql + " AND mp.Semester_Id = {semester_id} ".format(semester_id=semester.id)

        if 'partner_code' in args:
            sql = sql + "AND pa.Partner_Code = '{parner_code}' ".format(parner_code=args['partner_code'])

        if 'proposal_code' in args:
            sql = sql + "AND pc.Proposal_Code = '{proposal_code}' ".format(proposal_code=args['proposal_code'])
        sql = sql + " GROUP BY pc.ProposalCode_Id "
        results = pd.read_sql(sql, conn)
        return [int(x) for x in list(results['Ids'].values)]


class ProposalCode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalCodeModel


class ProposalComment(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalCommentModel


class ProposalContact(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalContactModel


class ProposalGeneralInfo(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalGeneralInfoModel


class ProposalInactiveReason(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalInactiveReasonModel


class ProposalInvestigator(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalInvestigatorModel


class ProposalProgress(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalProgressModel


class ProposalSelfActivation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalSelfActivationModel


class ProposalStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalStatusModel


class ProposalTechReport(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalTechReportModel


# class ProposalText(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = ProposalTextModel


class ProposalType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalTypeModel

#
# class ProposalUncalibratedFabryPerot(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = ProposalUncalibratedFabryPerotModel


class ProposalWarning(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ProposalWarningModel


class Publication(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = PublicationModel

#
# class RejectedProposals(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = RejectedProposalsModel


class RequestData(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RequestDataModel


class RequestDataFormat(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RequestDataFormatModel


class Rss(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssModel


class RssArcRequirement(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssArcRequirementModel


class RssArtStation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssArtStationModel


class RssBeamSplitterOrientation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssBeamSplitterOrientationModel


class RssCalibration(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssCalibrationModel


class RssCalibrationRun(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssCalibrationRunModel


class RssCalibrationRunDetails(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssCalibrationRunDetailsModel


class RssCalibrationType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssCalibrationTypeModel


class RssConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssConfigModel


class RssCurrentFilters(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssCurrentFiltersModel


class RssCurrentMasks(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssCurrentMasksModel


class RssDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssDetectorModel


class RssDetectorCalc(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssDetectorCalcModel


class RssDetectorMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssDetectorModeModel


class RssDetectorWindow(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssDetectorWindowModel


class RssEtalonConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssEtalonConfigModel


class RssEtalonPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssEtalonPatternModel


class RssEtalonPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssEtalonPatternDetailModel


class RssExposureType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssExposureTypeModel


class RssFabryPerot(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssFabryPerotModel

#
# class RssFabryPerotA(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = RssFabryPerotAModel


class RssFabryPerotCalibration(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssFabryPerotCalibrationModel


class RssFabryPerotCalibrationLine(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssFabryPerotCalibrationLineModel

#
# class RssFabryPerotFilterLine(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = RssFabryPerotFilterLineModel


class RssFabryPerotMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssFabryPerotModeModel


# class RssFabryPerotX(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = RssFabryPerotXModel
#
#
# class RssFabryPerotXY(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = RssFabryPerotXYModel
#
#
# class RssFabryPerotY(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = RssFabryPerotYModel


class RssFilter(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssFilterModel


class RssFlatRequirement(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssFlatRequirementModel


class RssGain(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssGainModel


class RssGrating(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssGratingModel


class RssHwPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssHwPatternModel


class RssHwPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssHwPatternDetailModel


class RssMask(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssMaskModel


class RssMaskType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssMaskTypeModel


class RssMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssModeModel


class RssMosMaskDetails(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssMosMaskDetailsModel


class RssMosMaskLegacyPhase1Description(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssMosMaskLegacyPhase1DescriptionModel


class RssMosReferenceStar(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssMosReferenceStarModel


class RssMosSlitlet(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssMosSlitletModel


class RssNightlyCalibration(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssNightlyCalibrationModel


class RssParallelism(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssParallelismModel


class RssPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssPatternModel


class RssPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssPatternDetailModel


class RssPolarimetry(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssPolarimetryModel


class RssPolarimetryPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssPolarimetryPatternModel


class RssPredefinedMaskDetails(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssPredefinedMaskDetailsModel


class RssProcedure(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssProcedureModel


class RssProcedureType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssProcedureTypeModel


class RssQwPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssQwPatternModel


class RssQwPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssQwPatternDetailModel


class RssRoSpeed(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssRoSpeedModel


class RssScheduleRequirement(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssScheduleRequirementModel


class RssSpectroscopy(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssSpectroscopyModel


class RssStrayLight(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssStrayLightModel


class RssThroughputMeasurement(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssThroughputMeasurementModel


class RssWaveStation(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = RssWaveStationModel


class SaLog(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SaLogModel


class SaLog_temp(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SaLog_tempModel


# class SaltAstronomers(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = SaltAstronomersModel


class Salticam(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamModel


class SalticamCalibration(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamCalibrationModel


class SalticamCalibrationType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamCalibrationTypeModel


class SalticamCurrentFilters(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamCurrentFiltersModel


class SalticamDetector(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamDetectorModel


class SalticamDetectorMode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamDetectorModeModel


class SalticamExposureType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamExposureTypeModel


class SalticamFilter(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamFilterModel


class SalticamFilterPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamFilterPatternModel


class SalticamFilterPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamFilterPatternDetailModel


class SalticamFlatRequirement(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamFlatRequirementModel


class SalticamGain(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamGainModel


class SalticamNightlyCalibration(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamNightlyCalibrationModel


class SalticamPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamPatternModel


class SalticamPatternDetail(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamPatternDetailModel


class SalticamProcedure(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamProcedureModel


class SalticamRoSpeed(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamRoSpeedModel


class SalticamScheduleRequirement(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamScheduleRequirementModel


class SalticamThroughputMeasurement(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamThroughputMeasurementModel


class SalticamWindow(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamWindowModel


class SalticamWindowPattern(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SalticamWindowPatternModel


class SaltOperator(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SaltOperatorModel


class SaltSubsystem(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SaltSubsystemModel


class SaltSubsystemTag(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SaltSubsystemTagModel


class schedule(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = scheduleModel


class Semester(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SemesterModel


class SemesterPhase(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SemesterPhaseModel


class SlotmodeEndData(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SlotmodeEndDataModel


# class SoLog(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = SoLogModel


class SoLogEvent(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SoLogEventModel


class StepStats(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = StepStatsModel


class StepTimeAccounting(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = StepTimeAccountingModel


class SubBlock(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SubBlockModel


class SubSubBlock(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = SubSubBlockModel


class TacProposalComment(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TacProposalCommentModel


class Tag(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TagModel


class Target(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetModel


class TargetConflict(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetConflictModel


class TargetCoordinates(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetCoordinatesModel


class TargetMagnitudes(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetMagnitudesModel


class TargetSubType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetSubTypeModel


class TargetType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TargetTypeModel


class TelescopeConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TelescopeConfigModel


class TelescopeConfigObsConfig(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TelescopeConfigObsConfigModel

#
# class temp(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = tempModel
#
#
# class temp3(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = temp3Model
#
#
# class temp_codes(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = temp_codesModel


# class temp_proposal(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = temp_proposalModel


class ThesisType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ThesisTypeModel


class Throughput(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ThroughputModel


class TimeBase(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TimeBaseModel


class TimeDiscountedReason(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TimeDiscountedReasonModel


# class TimeLostEvent(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = TimeLostEventModel


class TimeLostReason(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TimeLostReasonModel


class TimeRestricted(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TimeRestrictedModel


# class tmp(SQLAlchemyObjectType):
#     class Meta:
#         interfaces = (relay.Node, )
#         model = tmpModel


class ToDo(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ToDoModel


class ToDoPriority(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ToDoPriorityModel


class ToDoStatus(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ToDoStatusModel


class ToDoType(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = ToDoTypeModel


class Track(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TrackModel


class Transparency(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = TransparencyModel


class UncalibratedFabryPerot(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = UncalibratedFabryPerotModel


class Weather(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = WeatherModel


class WeatherEvent(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node, )
        model = WeatherEventModel


list_to_map = [
    ArcBible,
    ArcExposure,
    # AvailableDitherPatterns,
    Bandpass,
    BlindOffset,
    Block,
    BlockChange,
    BlockCode,
    # BlockPointWindow,
    BlockPool,
    # BlockProbabilities,
    BlockRejectedReason,
    # BlockScore,
    # BlockScoreTonight,
    BlockStatus,
    BlockType,
    # BlockVisibilityWindow,
    # BlockVisibilityWindow_AnyMoon,
    BlockVisibilityWindowType,
    BlockVisit,
    BlockVisitStatus,
    # BlockWeights,
    ButtonClass,
    Bvit,
    BvitFilter,
    BvitMode,
    BvitNeutralDensity,
    BvitPattern,
    BvitPatternDetail,
    CalFilter,
    CalibrationType,
    Commissioning,
    Concam,
    DatabaseVersion,
    Dimm,
    DitherPattern,
    DQ_FlatfieldAmpEdge,
    DQ_HrsArc,
    DQ_HrsOrder,
    DQ_RssArcIntensity,
    DQ_RssGain,
    DQ_SalticamGain,
    EventSource,
    EventType,
    Fault,
    FaultComment,
    # FaultCommentDiff,
    # FaultDiff,
    FaultRevision,
    FaultSeverity,
    FaultStatus,
    FaultSystemUser,
    # FaultTag,
    FaultType,
    FaultTypeTag,
    FileData,
    FindingChart,
    FitsHeaderHrs,
    FitsHeaderImage,
    FitsHeaderPipeline,
    FitsHeaderRss,
    FitsHeaderSalticam,
    # FixSoLogEvent,
    GuideMethod,
    GuideStar,
    Handover,
    HandoverStatus,
    HorizonsTarget,
    Hrs,
    HrsBlueDetector,
    HrsCalibrationType,
    HrsConfig,
    HrsExposurePattern,
    HrsExposurePatternDetail,
    HrsExposureType,
    HrsIodineCellPosition,
    HrsMode,
    HrsNightlyCalibration,
    HrsNodAndShuffle,
    HrsPattern,
    HrsPatternDetail,
    HrsProcedure,
    HrsRedDetector,
    HrsRoAmplifiers,
    HrsRoSpeed,
    HrsTargetLocation,
    Institute,
    InstituteName,
    Investigator,
    Lamp,
    MassDimm,
    MirrorAlignmentEvent,
    Moon,
    MovingGuideStar,
    MovingTable,
    MovingTableFile,
    MovingTarget,
    MultiPartner,
    NightInfo,
    NightLogs,
    NightlogSingleSection,
    # ObjectAvailability,
    ObsConfig,
    Observation,
    ObservingWindow,
    ObsLogTable,
    OcsHrsBlueDetector,
    OcsHrsBlueExposurePattern,
    OcsHrsConfig,
    OcsHrsProcedure,
    OcsHrsRedDetector,
    OcsHrsRedExposurePattern,
    OcsPayloadConfig,
    OcsRssConfig,
    OcsRssDetector,
    OcsRssDetectorWindow,
    OcsRssEtalonPattern,
    OcsRssFocusPattern,
    OcsRssHwPattern,
    # OcsRssMosReferenceStar,
    OcsSalticamDetector,
    OcsRssQwPattern,
    OcsSalticamConfig,
    OcsSalticamDetector,
    OcsSalticamProcedure,
    OcsSalticamProcedurePattern,
    OcsSalticamWindow,
    OcsStep,
    OcsTargetInformation,
    OcsTelescopeConfig,
    P1Bvit,
    P1BvitSimulation,
    P1Config,
    # P1ExternalFunding,
    P1Hrs,
    P1HrsSimulation,
    P1MinTime,
    P1ObservingConditions,
    P1ObservingWindow,
    P1OptionalTargets,
    P1P2Diff,
    P1P2DiffType,
    P1PreviousProposalStatus,
    P1ProposalTarget,
    P1RequestedTime,
    P1Rss,
    P1RssFabryPerot,
    P1RssMask,
    P1RssPolarimetry,
    P1RssSimulation,
    P1RssSpectroscopy,
    P1Salticam,
    P1SalticamFilterPattern,
    P1SalticamFilterPatternDetail,
    P1SalticamSimulation,
    # P1TargetProbabilities,
    P1Thesis,
    P1ToO,
    Partner,
    PartnerShareTimeDist,
    PayloadConfig,
    PayloadConfigType,
    PeriodicTarget,
    PeriodTimeDist,
    # PetriTemp,
    PhaseConstraint,
    PipelineConfig,
    PipelineDataAccessMethod,
    # PipelineDataQuality_CCD,
    PipelineDocFormat,
    PipelineProposalStatistics,
    PipelineStatistics,
    PipelineStatus,
    PiptAsyncProposalCode,
    PiptDisplayMode,
    PiptDisplayModeType,
    PiptEmailValidation,
    PiptErrorLog,
    PiptMailQueue,
    PiptNews,
    PiptSaltTAC,
    PiptSavedQuery,
    PiptSetting,
    PiptUser,
    PiptUserSetting,
    PiptUserTAC,
    PiptVersions,
    PiRanking,
    PointEvent,
    Pointing,
    Pool,
    PoolAssignedTime,
    PoolRule,
    # PoolRuleSet,
    PriorityAlloc,
    Proposal,
    ProposalCode,
    ProposalComment,
    ProposalContact,
    ProposalGeneralInfo,
    ProposalInactiveReason,
    ProposalInvestigator,
    ProposalProgress,
    ProposalSelfActivation,
    ProposalStatus,
    ProposalTechReport,
    # ProposalText,
    ProposalType,
    # ProposalUncalibratedFabryPerot,
    ProposalWarning,
    Publication,
    # RejectedProposals,
    RequestData,
    RequestDataFormat,
    Rss,
    RssArcRequirement,
    RssArtStation,
    RssBeamSplitterOrientation,
    RssCalibration,
    RssCalibrationRun,
    RssCalibrationRunDetails,
    RssCalibrationType,
    RssConfig,
    RssCurrentFilters,
    RssCurrentMasks,
    RssDetector,
    RssDetectorCalc,
    RssDetectorMode,
    RssDetectorWindow,
    RssEtalonConfig,
    RssEtalonPattern,
    RssEtalonPatternDetail,
    RssExposureType,
    RssFabryPerot,
    # RssFabryPerotA,
    RssFabryPerotCalibration,
    RssFabryPerotCalibrationLine,
    # RssFabryPerotFilterLine,
    RssFabryPerotMode,
    # RssFabryPerotX,
    # RssFabryPerotXY,
    # RssFabryPerotY,
    RssFilter,
    RssFlatRequirement,
    RssGain,
    RssGrating,
    RssHwPattern,
    RssHwPatternDetail,
    RssMask,
    RssMaskType,
    RssMode,
    RssMosMaskDetails,
    RssMosMaskLegacyPhase1Description,
    RssMosReferenceStar,
    RssMosSlitlet,
    RssNightlyCalibration,
    RssParallelism,
    RssPattern,
    RssPatternDetail,
    RssPolarimetry,
    RssPolarimetryPattern,
    RssPredefinedMaskDetails,
    RssProcedure,
    RssProcedureType,
    RssQwPattern,
    RssQwPatternDetail,
    RssRoSpeed,
    RssScheduleRequirement,
    RssSpectroscopy,
    RssStrayLight,
    RssThroughputMeasurement,
    RssWaveStation,
    SaLog,
    SaLog_temp,
    # SaltAstronomers,
    Salticam,
    SalticamCalibration,
    SalticamCalibrationType,
    SalticamCurrentFilters,
    SalticamDetector,
    SalticamDetectorMode,
    SalticamExposureType,
    SalticamFilter,
    SalticamFilterPattern,
    SalticamFilterPatternDetail,
    SalticamFlatRequirement,
    SalticamGain,
    SalticamNightlyCalibration,
    SalticamPattern,
    SalticamPatternDetail,
    SalticamProcedure,
    SalticamRoSpeed,
    SalticamScheduleRequirement,
    SalticamThroughputMeasurement,
    SalticamWindow,
    SalticamWindowPattern,
    SaltOperator,
    SaltSubsystem,
    SaltSubsystemTag,
    schedule,
    Semester,
    SemesterPhase,
    SlotmodeEndData,
    # SoLog,
    SoLogEvent,
    StepStats,
    StepTimeAccounting,
    SubBlock,
    SubSubBlock,
    TacProposalComment,
    Tag,
    Target,
    TargetConflict,
    TargetCoordinates,
    TargetMagnitudes,
    TargetSubType,
    TargetType,
    TelescopeConfig,
    TelescopeConfigObsConfig,
    # temp,
    # temp3,
    # temp_codes,
    # temp_proposal,
    ThesisType,
    Throughput,
    TimeBase,
    TimeDiscountedReason,
    # TimeLostEvent,
    TimeLostReason,
    TimeRestricted,
    # tmp,
    ToDo,
    ToDoPriority,
    ToDoStatus,
    ToDoType,
    Track,
    Transparency,
    UncalibratedFabryPerot,
    Weather,
    WeatherEvent,

]