from flask import g
from data import sdb_connect
from util.action import Action
from util.multipartner import multipartner_ids


def check_time_allocations(allocations, partner, semester):
    is_correct = False
    if not g.user.may_perform(Action.UPDATE_TIME_ALLOCATIONS, partner, semester):
        return is_correct

    is_correct = True
    for alloc in allocations:
        if isinstance(alloc["time"], float) or isinstance(alloc["time"], int):
            if alloc["time"] < 0 \
                    or alloc["priority"] not in [0, 1, 2, 3, 4] \
                    or not isinstance(alloc["proposal_code"], str):
                is_correct = False  # proposal have meet minimum requirements

    return is_correct


def update_time_allocations(partner, semester, time_allocations, tac_comments):
    """
    Update the database with a list of time allocations.

    Parameters
    ----------
    partner : str
        The partner code of the partner for whom the time allocations are updated.
    semester : str
        The semester, such as `2017-2` or `2018-1`, for which the time allocations are updated.
    time_allocations : iterable
        The list of time allocations. Each time allocation must be a dictionary with a proposal code, a priority
        and a time in seconds, such as `{'proposal_code': '2017-2-SCI-042', 'priority': 2, 'time': 2400}`.
    tac_comments : iterable
        The list of tac comments. Each tac comment must be a dictionary with a proposal code and a comment,
        such as `{'proposal_code': '2017-2-SCI-042', 'comment': 'this is a tac comment for this proposal'}`.

    """
    print(tac_comments)
    proposal_codes = [alloc['proposal_code'] for alloc in time_allocations]
    multipartner_id_map = multipartner_ids(proposal_codes, partner, semester)

    if not check_time_allocations(time_allocations, partner, semester):
        return False

    # FIXME: hard-coded id
    moon_id = 6

    # list of values in the form '(proposal code, priority, time in seconds)
    values_list = ['({multipartner_id}, {priority}, {time}, {moon_id})'
                       .format(multipartner_id=int(multipartner_id_map[alloc['proposal_code']]),
                               priority=int(alloc['priority']),
                               time=int(alloc['time']),
                               moon_id=int(moon_id))
                   for alloc in time_allocations
                   if alloc['proposal_code'] in multipartner_id_map.keys()]
    sql = '''INSERT INTO PriorityAlloc (MultiPartner_Id, Priority, TimeAlloc, Moon_Id)
                    VALUES {values}
                    ON DUPLICATE KEY UPDATE
                        MultiPartner_Id=VALUES(MultiPartner_Id),
                        Priority=VALUES(Priority),
                        TimeAlloc=VALUES(TimeAlloc),
                        Moon_Id=VALUES(Moon_Id)'''.format(values=', '.join(values_list))

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
            cursor.execute(sql)
            cursor.execute(tac_comment_sql)
            connection.commit()
    except:
        return False
    finally:
        connection.close()
    return True
