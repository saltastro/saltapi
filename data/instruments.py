import pandas as pd
from data import sdb_connect


def get_instruments(proposal_ids, proposals):
    from schema.instruments import RSS, HRS, BVIT, SCAM, Spectroscopy, Polarimetry, FabryPerot, Mask

    instruments_sql = '''
SELECT
    *,
    sc.DetectorMode AS SCDetectorMode,
    sc.XmlDetectorMode AS SCXmlDetectorMode,
    rs.DetectorMode AS RSDetectorMode,
    rs.XmlDetectorMode AS RSXmlDetectorMode
FROM P1Config
    JOIN ProposalCode USING(ProposalCode_Id)
        LEFT JOIN P1Rss using(P1Rss_Id)
        LEFT JOIN RssDetectorMode AS rs USING(RssDetectorMode_Id)
        LEFT JOIN RssMode USING(RssMode_Id)
        LEFT JOIN P1RssSpectroscopy USING(P1RssSpectroscopy_Id)
        LEFT JOIN RssGrating USING(RssGrating_Id)
        LEFT JOIN P1RssFabryPerot USING(P1RssFabryPerot_Id)
        LEFT JOIN RssFabryPerotMode USING(RssFabryPerotMode_Id)
        LEFT JOIN RssEtalonConfig USING(RssEtalonConfig_Id)
        LEFT JOIN P1RssPolarimetry USING(P1RssPolarimetry_Id)
        LEFT JOIN RssPolarimetryPattern USING(RssPolarimetryPattern_Id)
        LEFT JOIN P1RssMask USING(P1RssMask_Id)
        LEFT JOIN RssMaskType USING(RssMaskType_Id)
        LEFT JOIN P1Salticam USING(P1Salticam_Id)
        LEFT JOIN SalticamDetectorMode AS sc USING(SalticamDetectorMode_Id)
        LEFT JOIN P1Bvit USING(P1Bvit_Id)
        LEFT JOIN BvitFilter USING(BvitFilter_Id)
        LEFT JOIN P1Hrs USING(P1Hrs_Id)
        LEFT JOIN HrsMode USING(HrsMode_Id)
WHERE ProposalCode_Id IN {proposal_ids}
'''.format(proposal_ids=proposal_ids)

    conn = sdb_connect()

    i_results = pd.read_sql(instruments_sql, conn)

    conn.close()
    for index, row in i_results.iterrows():
        try:
            if not pd.isnull(row["P1Rss_Id"]):
                proposals[row["Proposal_Code"]].instruments.append(
                    RSS(
                        type="RSS",
                        detector_mode=row['RSDetectorMode'],
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
                            waveplate_pattern=row['PatternName']
                        ),
                        mask=Mask(
                            type=row['RssMaskType'],
                            mos_description=row['MosDescription']
                        )
                    )
                )
            if not pd.isnull(row["P1Hrs_Id"]):
                proposals[row["Proposal_Code"]].instruments.append(
                    HRS(
                        type="HRS",
                        detector_mode=row["ExposureMode"]
                    )
                )
            if not pd.isnull(row["P1Bvit_Id"]):
                proposals[row["Proposal_Code"]].instruments.append(
                    BVIT(
                        type="BVIT",
                        filter=row['BvitFilter_Name']
                    )
                )
            if not pd.isnull(row["P1Salticam_Id"]):
                proposals[row["Proposal_Code"]].instruments.append(
                    SCAM(
                        type="SCAM",
                        detector_mode=row['SCDetectorMode']
                    )
                )
        except KeyError:
            pass