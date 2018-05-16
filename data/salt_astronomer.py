import pandas as pd
from data import sdb_connect


def get_salt_astronomers():
    from schema.user import User
    conn = sdb_connect()
    sql = """
            select * from SaltAstronomers
                join Investigator using (Investigator_Id)
                join PiptUser using (Investigator_Id)
            where FirstName != "Techops"
        """
    astronomers = [User(
        first_name=row["FirstName"],
        last_name=row["Surname"],
        email=row["Email"],
        username=row["Username"]
    ) for i, row in pd.read_sql(sql, conn).iterrows()]

    conn.close()

    return astronomers
