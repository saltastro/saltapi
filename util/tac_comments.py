from flask import g
from data import sdb_connect
from util.action import Action
from util.multipartner import multipartner_ids

def update_tac_comments(tac_comments, partner, semester):
    """
    Update the database with a list of tac comments.

    Parameters
    ----------
    tac_comments : iterable
        The list of time allocations. Each time allocation must be a dictionary with a proposal code, a priority
        and a time in seconds, such as `{'proposal_code': '2017-2-SCI-042', 'priority': 2, 'time': 2400}`.
    partner : str
        The partner code of the partner for whom the time allocations are updated.
    semester : str
        The semester, such as `2017-2` or `2018-1`, for which the time allocations are updated.

    """

    proposal_codes = [comme['proposal_code'] for comme in tac_comments]
    multipartner_id_map = multipartner_ids(proposal_codes, partner, semester)

    # list of values in the form '(proposal code, tac comment)

    comment_list = ['({multipartner_id}, "{tac_comment}")'
                        .format(multipartner_id=int(multipartner_id_map[comme['proposal_code']]),
                                tac_comment=str(comme['comment']))
                    for comme in tac_comments
                    if comme['proposal_code'] in multipartner_id_map.keys()]

    tac_comment_sql = '''INSERT INTO TacProposalComment (MultiPartner_Id, TacComment)
                        VALUES {values}
                        ON DUPLICATE KEY UPDATE
                            MultiPartner_Id=VALUES(MultiPartner_Id),
                            TacComment=VALUES(TacComment)'''.format(values=', '.join(comment_list))
    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(tac_comment_sql)
            connection.commit()
            pass
    finally:
        connection.close()

    return True
