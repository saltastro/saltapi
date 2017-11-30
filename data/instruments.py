from pymysql.connections import Connection
import pandas as pd
from data import sdb_connect


def get_instruments(ids, proposals):
    from schema.instruments import RSS, HRS, BVIT, SCAM, Spectroscopy, Polarimetry, FabryPerot, Mask

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
                      '   left join P1Hrs using(P1Hrs_Id) ' \
                      '   left join HrsMode using(HrsMode_Id) '
    if len(ids['ProposalIds']) == 1:
        instruments_sql += "  where ProposalCode_Id = {id}".format(id=ids['ProposalCode_Ids'][0])
    else:
        instruments_sql += "  where ProposalCode_Id in {ids}".format(ids=tuple(ids['ProposalCode_Ids']))
    conn = sdb_connect()

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
