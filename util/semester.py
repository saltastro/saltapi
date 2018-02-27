def previous_semester(semester):
    """
    The semester before the given one.

    Parameters
    ----------
    semester : str
        Semester, such as '2018-1'.

    Returns
    -------
    previous : str
        The previous semester.

    Examples
    --------
    >>> previous_semester('2018-1')
    '2017-2'
    >>> previous_semester('2017-2')
    '2017-1'
    """

    year, sem = semester.split('-')
    year = int(year)
    sem = int(sem)

    if sem == 1:
        year -= 1
        sem = 2
    elif sem == 2:
        sem = 1
    else:
        raise ValueError('Semester must be 1 or 2. Found: {sem}'.format(sem=sem))

    return '{year}-{sem}'.format(year=year, sem=sem)