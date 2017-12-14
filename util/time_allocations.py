import pandas as pd
from data import sdb_connect

def multipartner_ids(proposal_codes, partner, semester):
    """
    Map proposal codes to multipartner ids.

    Proposal codes are ignored if the proposal doesn't have a multipartner entry for the partner and semester.

    Parameters
    ----------
    proposal_codes : iterable
        The proposal codes to map.
    partner : str
        The partner code, such as `RSA` or `IUCAA`.
    semester : str
        The semester, such as `2017-2` or `2018-1`.

    Returns
    -------
    ids: dict
       A dictionary of proposal codes and multipartner ids.
    """

    year, sem = semester.split('-')
    proposal_code_strings = ["'{proposal_code}'".format(proposal_code=proposal_code)
                             for proposal_code in proposal_codes]
    sql = '''SELECT pc.Proposal_Code, mp.MultiPartner_Id
                    FROM MultiPartner AS mp
                    JOIN ProposalCode AS pc USING (ProposalCode_Id)
                    JOIN Partner AS p USING (Partner_Id)
                    JOIN Semester AS s USING (Semester_Id)
                    WHERE pc.Proposal_Code IN ({proposal_codes})
                          AND p.Partner_Code='{partner_code}'
                          AND (s.Year={year} AND s.Semester={semester})'''.format(
        proposal_codes=', '.join(proposal_code_strings),
        partner_code=partner,
        year=year,
        semester=sem)

    df = pd.read_sql(sql, sdb_connect())

    return {item['Proposal_Code']: item['MultiPartner_Id'] for item in df.to_dict('records')}

def update_time_allocations(time_allocations, partner, semester):
    """
    Update the database with a list of time allocations.

    Parameters
    ----------
    time_allocations : iterable
        The list of time allocations. Each time allocation must be a dictionary with a proposal code, a priority
        and a time in seconds, such as `{'proposal_code': '2017-2-SCI-042', 'priority': 2, 'time': 2400}`.
    partner : str
        The partner code of the partner for whom the time allocations are updated.
    semester : str
        The semester, such as `2017-2` or `2018-1`, for which the time allocations are updated.

    """

    proposal_codes = [alloc['proposal_code'] for alloc in time_allocations]
    multipartner_id_map = multipartner_ids(proposal_codes, partner, semester)

    # TODO: Perform checks!

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

    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()

    return True
