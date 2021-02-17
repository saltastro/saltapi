from datetime import datetime
import pandas as pd

from data import sdb_connect


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


def current_semester():
    """
    the current semester

    Returns
    -------
    semester : dict
        The current semester.
    """

    date = datetime.now().date()
    sql = """
SELECT Semester_Id, Year, Semester
    FROM Semester
WHERE StartSemester <= "{date}" AND EndSemester >= "{date}"
""".format(date=date)
    results = pd.read_sql(sql, sdb_connect())
    sdb_connect().close()
    return {
        "semester": '{year}-{sem}'.format(year=results.iloc[0]["Year"], sem=results.iloc[0]["Semester"]),
        "semester_id": int(results.iloc[0]["Semester_Id"])
    }


def query_semester_id(semester):
    sql = """
    SELECT Semester_Id FROM Semester WHERE CONCAT(Year, "-",Semester) = %(semester)s
    """
    df = pd.read_sql(sql, con=sdb_connect(), params={"semester": semester})
    if df.empty:
        raise ValueError("Semester '{semester}' is not known".format(semester=semester))
    return int(df["Semester_Id"][0])
