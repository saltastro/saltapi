import pandas as pd
from data import sdb_connect


def get_salt_astronomer():
    from schema.salt_astronomer import SALTAstronomer
    conn = sdb_connect()
    sql = """
            select * from SaltAstronomers
                join Investigator using (Investigator_Id)
                join PiptUser using (Investigator_Id)
            where FirstName != "Techops"
        """
    astros = [SALTAstronomer(
        name=row["FirstName"],
        surname=row["Surname"],
        email=row["Email"],
        username=row["Username"]
    ) for i, row in pd.read_sql(sql, conn).iterrows()]

    conn.close()

    return astros
