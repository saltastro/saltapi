import pandas as pd
from data import sdb_connect


def get_selectors_data():
    from schema.selectors import Selectors

    sem = 'select CONCAT(Year,"-", Semester) as Semester from Semester '
    par = 'select Partner_Code from Partner'
    conn = sdb_connect()
    try:
        sem_results = pd.read_sql(sem, conn)
        par_results = pd.read_sql(par, conn)
        conn.close()

        return Selectors(
            semester=[row['Semester'] for index, row in sem_results.iterrows()],
            partner=[row['Partner_Code'] for index, row in par_results.iterrows()]
        )
    except:
        raise RuntimeError("Fail to get selectors data")


