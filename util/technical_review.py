from data import sdb_connect
from data.technical_review import update_technical_report, update_liaison_astronomer


def update_tech_comments(semester, S_a_l_t_astronomer, tech_comments):
    """
    Update the database with a list of time allocations.

    Parameters
    ----------
    semester : str
        The semester, such as `2017-2` or `2018-1`, for which the time allocations are updated.
    S_a_l_t_astronomer : str
        this is a salt astronomer username
    tech_comments : iterable
        The list of tech comments. Each tech comment must be a dictionary with a proposal code and a comment,
        such as `{'proposal_code': '2017-2-SCI-042', 'comment': 'this is a tac comment for this proposal'}`.

    """
    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for tech in tech_comments:
                update_technical_report(proposal_code=tech['proposal_code'], semester=semester, report=tech['comment'], cursor=cursor)
            connection.commit()
    except:
        return False
    finally:
        connection.close()
    return True


def update_liaison_astronomers(semester, proposals_assigned):
    """
    Update the database with a list of time allocations.

    Parameters
    ----------
    semester : str
        The semester, such as `2017-2` or `2018-1`, for which the time allocations are updated.
    proposals_assigned : List
        ####TODO
    """
    connection = sdb_connect()
    try:
        with connection.cursor() as cursor:
            for assigned in proposals_assigned:
                liaison = assigned['liaison_astronomer']
                for proposal in assigned['proposals']:
                    update_liaison_astronomer(proposal_code=proposal, liaison_astronomer=liaison, cursor=cursor)
            connection.commit()
    except:
        return False
    finally:
        connection.close()
    return True
