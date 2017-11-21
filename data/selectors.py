import pandas as pd
from data import conn


def get_selectors_data():
    from schema.selectors import Selectors

    sem = 'select CONCAT(Year,"-", Semester) as Semester from Semester '
    par = 'select Partner_Code from Partner'
    sem_results = pd.read_sql(sem, conn)
    par_results = pd.read_sql(par, conn)

    return Selectors(
        semester=[row['Semester'] for index, row in sem_results.iterrows()],
        partner=[row['Partner_Code'] for index, row in par_results.iterrows()]
    )


