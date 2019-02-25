import pandas as pd
from data import sdb_connect


def get_proposals_text(proposal_code_ids):
    proposals_text = {}
    proposals_text_sql = """
        SELECT * FROM ProposalText
        join ProposalCode using(ProposalCode_Id)
        WHERE ProposalCode_Id in {proposal_code_ids}
        order by Semester_Id desc """.format(proposal_code_ids=proposal_code_ids)
    conn = sdb_connect()
    for index, row in pd.read_sql(proposals_text_sql, conn).iterrows():
        if row["Proposal_Code"] not in proposals_text:
            proposals_text[row["Proposal_Code"]] = {
                "title": row["Title"], "abstract": row["Abstract"]
            }
    conn.close()
    return proposals_text
