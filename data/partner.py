import pandas as pd
from flask import g
from data import sdb_connect
from util.action import Data
from util.semester import current_semester, query_semester_id


def get_partners(semester, partner):
    from schema.partner import Partner, TimeAllocation, Priority

    sql = ''' 
SELECT * FROM  PeriodTimeDist
    JOIN Partner USING(Partner_Id)
    JOIN Semester USING(Semester_Id)
WHERE concat(Year,"-", Semester) = "{semester}"
'''.format(semester=semester)
    if partner is not None:
        sql += ' AND Partner_Code = "{partner_code}" '.format(partner_code=partner)

    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()

    partners = [Partner(
        id="Partner: " + str(row["Partner_Id"]),
        name=row["Partner_Name"],
        code=row["Partner_Code"],
        time_allocation=TimeAllocation(
            semester=str(row['Year']) + "-" + str(row['Semester']),
            used_time=Priority(
                p0_andp1=row['Used0and1'],
                p2=row['Used2'],
                p3=row['Used3']
            ),
            allocated_time=Priority(
                p0_andp1=row['Alloc0and1'],
                p2=row['Alloc2'],
                p3=row['Alloc3']
            )
        )) for index, row in results.iterrows()] if partner is not None else \
        [Partner(
            id="Partner: " + str(row["Partner_Id"]),
            name=row["Partner_Name"] if g.user.may_view(Data.AVAILABLE_TIME, partner=row["Partner_Code"]) else None,
            code=row["Partner_Code"] if g.user.may_view(Data.AVAILABLE_TIME, partner=row["Partner_Code"]) else None,
            time_allocation=TimeAllocation(
                semester=str(row['Year']) + "-" + str(row['Semester']),
                used_time=Priority(
                    p0_andp1=row['Used0and1'],
                    p2=row['Used2'],
                    p3=row['Used3']
                ),
                allocated_time=Priority(
                    p0_andp1=row['Alloc0and1'],
                    p2=row['Alloc2'],
                    p3=row['Alloc3']
                )
            )) for index, row in results.iterrows()]

    return partners


def get_partner_codes(only_partner_ids=None, semester=current_semester()["semester"]):
    """
    Parameters
    ----------
    only_partner_ids : Optional[list]
        Partner ID, .
    semester: Optional[int]

    """
    semester_id = query_semester_id(semester=semester)
    if semester_id > current_semester()["semester_id"]:
        semester_id = current_semester()["semester_id"]

    par = '''
SELECT Partner_Code FROM Partner
    JOIN PartnerShareTimeDist USING(Partner_Id)
    JOIN Semester USING(Semester_Id)
WHERE `Virtual` = 0
    AND Semester_Id = %s
    AND TimePercent > 0
    '''
    if only_partner_ids is not None:
        ids = [str(i) for i in only_partner_ids]
        par += ' AND Partner_Id IN ({ids})'.format(ids=", ".join(ids))
    conn = sdb_connect()
    results = pd.read_sql(par, conn, params=(semester_id,))
    conn.close()

    return [row["Partner_Code"] for i, row in results.iterrows()]


def get_partner_code_id(partner_code):
    sql = ''' 
SELECT Partner_Id FROM Partner WHERE Partner_Code = "{partner_code}"
    '''.format(partner_code=partner_code)
    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    if not results.empty:
        return results.iloc[0]["Partner_id"]
    raise ValueError("Partner 'partner_code' can not be found".format(partner_code=partner_code))