from schema.target import Target, Coordinates
from schema.proposals import Proposal
from schema.proposals import Proposal
import pandas as pd
from data import sdb_connect

def target(row):
    sign = -1 if row['DecSign'] == '-' else 1
    return Target(
            id="Target: " + str(row['Target_Id']),
            name=row['Target_Name'],
            optional=row['Optional'] == 1,
            proposal_code=row['Proposal_Code'],
            coordinates=Coordinates(
                ra=(row['RaH'] + row['RaM'] / 60 + row['RaS'] / 3600) / (24 / 360),
                dec=(sign * (row['DecD'] + row['DecM'] / 60 + row['DecS'] / 3600)))
        )


def get_targets(ids=None, proposals=None, semester=None, partner_code=None, proposal_code=None):
    """
        If you do not provide ids you must provide semester or vise versa. value error will be raised if none is provide.
        If both semester and ids are provide value error is raised.
        the idea was to get a list of target not depending on any proposals or put targets to respective 
        proposal but not both at the same time
    :param ids: 
    :param proposals: 
    :param semester: 
    :param partner_code: 
    :param proposal_code: 
    :return: 
    """
    if ids is not None and semester is not None:
        raise ValueError("targets are acquired by either ids or semester but not both")
    targets = {}
    if ids is None:
        if semester is None:
            raise ValueError("semester must be provided when query for Targets")
        ids = Proposal.get_proposal_ids(semester=semester, partner_code=partner_code, proposal_code=proposal_code)

    sql = "select * " \
          "  from Proposal" \
          "         join ProposalCode using (ProposalCode_Id) " \
          "         join P1ProposalTarget using (ProposalCode_Id) " \
          "         join Target as tp on (P1ProposalTarget.Target_Id = tp.Target_Id) " \
          "         join TargetCoordinates using(TargetCoordinates_Id) "
    if len(ids['ProposalIds']) == 1:
        sql += "  where Proposal_Id = {id} order by Proposal_Id".format(id=ids['ProposalIds'][0])
    else:
        sql += "  where Proposal_Id in {ids} order by Proposal_Id".format(ids=tuple(ids['ProposalIds']))

    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    for i, row in results.iterrows():
        if proposals is None:
            targets[row["Proposal_Code"]] = target(row)
        else:
            proposals[row["Proposal_Code"]].targets.append(target(row))

    return targets.values()
