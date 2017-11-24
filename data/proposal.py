from pymysql.connections import Connection
import pandas as pd
from data import sdb_connect
from schema.proposals import Proposal

proposal_data = {}


def query_proposal_data(**args):
    from schema.proposal import Proposals, RequestedTimeM, ProposalInfoM
    from schema.instruments import RSS, HRS, BVIT, SCAM, Instruments, Spectroscopy, Polarimetry, FabryPerot, Mask

    ids = Proposal.get_proposal_ids(**args)
    conn = sdb_connect()
    proposals = {}
    if isinstance(conn, Connection):
        proposal_sql = " select * from Proposal " \
                   "     join ProposalCode using (ProposalCode_Id) " \
                   "     join ProposalGeneralInfo using (ProposalCode_Id) " \
                   "     join P1RequestedTime as p1 using (Proposal_Id) " \
                   "     join Moon as mo on (mo.Moon_Id=p1.Moon_Id) " \
                   "     join ProposalStatus using (ProposalStatus_Id) " \
                   "     join Semester as s on (s.Semester_Id = p1.Semester_Id) " \
                   "     join P1ObservingConditions  using (ProposalCode_Id) " \
                   "     join Transparency using (Transparency_Id) " \
                   "     join ProposalContact as pc using(ProposalCode_Id) " \
                   "     join Investigator as i on(i.Investigator_Id = pc.Leader_Id) " \
                   "     left join P1Thesis using (ProposalCode_Id) " \
                   "     join P1MinTime using(ProposalCode_Id) " \
                   "  where Proposal_Id in {ids} order by Proposal_Id" \
                   " ".format(ids=tuple(ids['ProposalIds']))
        results = pd.read_sql(proposal_sql, conn)
        conn.close()

        pc = []  # I am using pc to control proposals that are checked
        for index, row in results.iterrows():
            if row["Proposal_Code"] not in pc:
                proposals[row["Proposal_Code"]] = Proposals(
                    id="Proposal: " + str(row["Proposal_Id"]),
                    code=row["Proposal_Code"],
                    general_info=ProposalInfoM(
                        is_p4=row["P4"] == 1,
                        status=row["Status"],
                        transparency=row["Transparency"],
                        max_seeing=row["MaxSeeing"]
                    ),
                    total_time_requested=row["TotalReqTime"],
                    minimum_useful_time=row["P1MinimumUsefulTime"],
                    time_requests=[],
                    instruments=Instruments(
                        rss=[],
                        hrs=[],
                        bvit=[],
                        scam=[]
                    ),
                    is_thesis=not pd.isnull(row["ThesisType_Id"])  # concluded that none thesis proposals have null on
                    # P1Thesis
                )
            proposals[row["Proposal_Code"]].time_requests.append(
                RequestedTimeM(
                    moon=row["Moon"],
                    time=row["P1RequestedTime"],
                    for_semester=str(row['Year']) + "-" + str(row['Semester'])
                )
            )
            pc.append(row["Proposal_Code"])  # I am using pc to control proposals that are checked

    instruments_sql = ' select *, sc.DetectorMode as SCDetectorMode, sc.XmlDetectorMode as SCXmlDetectorMode, ' \
                      '         rs.DetectorMode as RSDetectorMode, rs.XmlDetectorMode as RSXmlDetectorMode  ' \
                      '         from P1Config ' \
                      '   join ProposalCode using (ProposalCode_Id) ' \
                      '   left Join P1Rss using(P1Rss_Id) ' \
                      '   left join RssDetectorMode as rs using(RssDetectorMode_Id) ' \
                      '   left join RssMode using (RssMode_Id) ' \
                      '   left join P1RssSpectroscopy using (P1RssSpectroscopy_Id) ' \
                      '   left join RssGrating using (RssGrating_Id) ' \
                      '   left join P1RssFabryPerot using (P1RssFabryPerot_Id) ' \
                      '   left join RssFabryPerotMode using (RssFabryPerotMode_Id) ' \
                      '   left join RssEtalonConfig using (RssEtalonConfig_Id) ' \
                      '   left join P1RssPolarimetry using (P1RssPolarimetry_Id) ' \
                      '   left join RssPolarimetryPattern using (RssPolarimetryPattern_Id) ' \
                      '   left join P1RssMask using (P1RssMask_Id) ' \
                      '   left join RssMaskType using (RssMaskType_Id) ' \
                      '   ' \
                      '   left join P1Salticam using(P1Salticam_Id) ' \
                      '   left join SalticamDetectorMode as sc using(SalticamDetectorMode_Id) ' \
                      '    ' \
                      '   left join P1Bvit using(P1Bvit_Id) ' \
                      '   left join BvitFilter using(BvitFilter_Id) ' \
                      '    ' \
                      '   left join P1Hrs using(P1Hrs_Id) ' \
                      '   left join HrsMode using(HrsMode_Id) ' \
                      ' where ProposalCode_Id in {codes} order by Proposal_Code ' \
                      ''.format(codes=tuple(ids['ProposalCodes']))
    conn = sdb_connect()
    if isinstance(conn, Connection):
        i_results = pd.read_sql(instruments_sql, conn)
        conn.close()
        for index, row in i_results.iterrows():
            if not pd.isnull(row["P1Rss_Id"]):
                proposals[row["Proposal_Code"]].instruments.rss.append(
                    RSS(
                        type="RSS",
                        dictator_mode=row['RSDetectorMode'],
                        xml_dictator_mode=row['RSXmlDetectorMode'],
                        mode=row['Mode'],
                        spectroscopy=Spectroscopy(
                            grating=row["Grating"]
                        ),
                        fabry_perot=FabryPerot(
                            mode=row['FabryPerot_Mode'],
                            description=row['FabryPerot_Description'],
                            etalon_config=row['EtalonConfig'],
                        ),
                        polarimetry=Polarimetry(
                            pattern_name=row['PatternName']
                        ),
                        mask=Mask(
                            type=row['RssMaskType'],
                            mos_description=row['MosDescription']
                        )
                    )
                )
            if not pd.isnull(row["P1Hrs_Id"]):
                proposals[row["Proposal_Code"]].instruments.hrs.append(
                    HRS(
                        type="HRS",
                        exposure_mode=row["ExposureMode"]
                    )
                )
            if not pd.isnull(row["P1Bvit_Id"]):
                proposals[row["Proposal_Code"]].instruments.bvit.append(
                    BVIT(
                        type="BVIT",
                        filter_name=row['BvitFilter_Name']
                    )
                )
            if not pd.isnull(row["P1Salticam_Id"]):
                proposals[row["Proposal_Code"]].instruments.scam.append(
                    SCAM(
                        type="SCAM",
                        dictator_mode=row['SCDetectorMode'],
                        xml_dictator_mode=row['SCXmlDetectorMode']
                    )
                )
    return proposals.values()


def get_proposals(**args):
    data = query_proposal_data(**args)
    return data
