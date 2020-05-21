from pandas._libs.tslib import NaTType
from schema.target import Target, Position, Magnitude
from data.common import sql_list_string, get_all_proposal_ids, get_user_viewable_proposal_ids
import pandas as pd
from data import sdb_connect


def target(row):
    """
    :param row: a target query row (A pandas Series)
    :return: Target Object (mapped only data need by TAC process)
    """
    sign = -1 if row['DecSign'] == '-' else 1
    return Target(
        id="Target: " + str(row['Target_Id']),
        name=row['Target_Name'],
        is_optional=row['Optional'] == 1,
        position=Position(
            ra=(row['RaH'] + row['RaM'] / 60 + row['RaS'] / 3600) / (24 / 360),
            dec=(sign * (row['DecD'] + row['DecM'] / 60 + row['DecS'] / 3600)),
            ra_dot=None if isinstance(row['Epoch'], NaTType) else row['RaDot'],
            dec_dot=None if isinstance(row['Epoch'], NaTType) else row['DecDot'],
            epoch=None if isinstance(row['Epoch'], NaTType) else row['Epoch']
        ),
        magnitude=Magnitude(
            filter=row['FilterName'],
            min_magnitude=row['MinMag'],
            max_magnitude=row['MaxMag']
        )
    )


def get_targets(proposal_code_ids=None, proposals=None, semester=None, partner_code=None):
    """
        If you do not provide ids you must provide semester or vise versa. value error will be raised if none is
            provide.
        If both semester and ids are provide value error is raised.
            The idea is to get a list of target not depending on any proposals or put targets to respective
            proposal but not both at the same time

    :param proposal_code_ids: Ids need to be provided by Proposals class (if you need a list of targets in a proposal)
                                        ==> Todo need to be moved
    :param proposals: Dict of proposals with they code as keys (if you need a list of targets in a proposal)
    :param semester: semester querying for (if you need a list of targets)
    :param partner_code: partner querying for (if you need a list of targets)
    :return: list of targets (used by graphQL query) (if you need a list of targets)
    """
    if proposal_code_ids is not None and semester is not None:
        raise ValueError("targets are acquired by either ids or semester but not both")
    targets = []
    if proposal_code_ids is None:
        if semester is None:
            raise ValueError("semester must be provided when query for Targets")
        proposal_code_ids = sql_list_string(
            get_all_proposal_ids(semester=semester, partner_code=partner_code)["ProposalCode_Id"].tolist()
        ) if partner_code is None \
            else sql_list_string(
            get_user_viewable_proposal_ids(semester=semester, partner_code=partner_code)
        )
    sql = """
     SELECT distinct Target_Id, Proposal_Code, DecSign, Target_Name, Optional, RaH, RaM, RaS, 
     DecD, DecM, DecS, Epoch, RaDot, DecDot, FilterName, MinMag, MaxMag
        FROM Proposal
            JOIN P1ProposalTarget USING (ProposalCode_Id)
            JOIN ProposalCode USING (ProposalCode_Id)
            JOIN Target USING (Target_Id)
            JOIN TargetCoordinates USING(TargetCoordinates_Id)
            JOIN TargetMagnitudes USING(TargetMagnitudes_Id)
            JOIN Bandpass USING(Bandpass_Id)
            LEFT JOIN MovingTarget USING(MovingTarget_Id)
        WHERE ProposalCode_Id IN {proposal_code_ids} ORDER BY ProposalCode_Id
     """.format(proposal_code_ids=proposal_code_ids)

    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()

    for i, row in results.iterrows():
        try:
            if proposals is None:
                targets.append(target(row))
            else:
                proposals[row["Proposal_Code"]].targets.append(target(row))
        except KeyError:
            pass
    return targets
