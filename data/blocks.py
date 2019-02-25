import pandas as pd
from data import sdb_connect


def get_blocks_status(proposal_code, blocks_status_id):
    """
    Queries the blocks status for a specific proposal and returns the blocks code with the specified status.
    :param proposal_code:
    :param blocks_status_id:
    :return: array
    """

    sql = '''SELECT BlockCode AS block_code
FROM Block
JOIN BlockCode USING (BlockCode_Id)
JOIN ProposalCode USING (ProposalCode_Id)
JOIN BlockStatus USING (BlockStatus_Id)
WHERE Proposal_Code=%s
AND BlockStatus_Id=%s'''
    df = pd.read_sql(sql, params=(proposal_code, blocks_status_id,), con=sdb_connect())

    return df['block_code'].to_dict()
