import pandas as pd
from data.common import sdb_connect


def get_user_details(user_id):

    sql = '''
SELECT
    u.Username, i.FirstName, i.Surname, i.Email
FROM PiptUser AS u
    JOIN Investigator AS i using (Investigator_Id)
WHERE u.PiptUser_Id = {user_id}
'''.format(user_id=user_id)
    conn = sdb_connect()
    user_details_results = pd.read_sql(sql, conn)
    conn.close()
    print(user_details_results.iloc[0])
    if not user_details_results.empty:
        return {
            "user_id": user_id,
            "username": user_details_results.iloc[0]["Username"],
            "first_name": user_details_results.iloc[0]["FirstName"],
            "last_name": user_details_results.iloc[0]["Surname"],
            "email": user_details_results.iloc[0]["Email"]
        }
    return None
