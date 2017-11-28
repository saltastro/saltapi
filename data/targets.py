from schema.target import Target, Coordinates
from schema.proposals import Proposal
import pandas as pd
from data import sdb_connect


def get_targets(ids, proposals):
    targets = {}

    sql = "".format(ids["proposalCode_Ids"])  # Todo Add sql query
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    for i, row in results.iterrows():
        sign = -1 if row['DecSign'] == '-' else 1
        targets[row["proposal_Code"]] = Target(
            id=row[''],
            name=row[''],
            optional=row[''],
            coordinates=Coordinates(
                ra=(row['RaH'] + row['RaM'] / 60 + row['RaS'] / 3600) / (24 / 360),
                dec=(sign * (row['DecD'] + row['DecM'] / 60 + row['DecS'] / 3600))),

        )
