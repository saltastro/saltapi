import pandas as pd
from flask import g
from data import sdb_connect
from schema.user import RoleType


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
        allocated_time=TimeAllocation(
            semester=str(row['Year']) + "-" + str(row['Semester']),
            used_time=Priority(
                p0_p1=row['Used0and1'],
                p2=row['Used2'],
                p3=row['Used3']
            ),
            allocated_time=Priority(
                Allocated_p0_p1=row['Alloc0and1'],
                Allocated_p2=row['Alloc2'],
                Allocated_p3=row['Alloc3']
            )
        )) for index, row in results.iterrows()] if partner is not None else \
        [Partner(
            id="Partner: " + str(row["Partner_Id"]),
            name=row["Partner_Name"] if g.user.has_role(RoleType.ADMINISTRATOR, row["Partner_Code"]) else None,
            code=row["Partner_Code"] if g.user.has_role(RoleType.ADMINISTRATOR, row["Partner_Code"]) else None,
            allocated_time=TimeAllocation(
                semester=str(row['Year']) + "-" + str(row['Semester']),
                used_time=Priority(
                    p0_p1=row['Used0and1'],
                    p2=row['Used2'],
                    p3=row['Used3']
                ),
                allocated_time=Priority(
                    Allocated_p0_p1=row['Alloc0and1'],
                    Allocated_p2=row['Alloc2'],
                    Allocated_p3=row['Alloc3']
                )
            )) for index, row in results.iterrows()]

    return partners


def get_partners_for_role(ids=None):
    par = 'SELECT Partner_Code FROM Partner '
    if ids is not None:
        ids = [str(id) for id in ids]
        par += ' WHERE Partner_Id IN ({ids})'.format(ids=", ".join(ids))

    conn = sdb_connect()
    results = pd.read_sql(par, conn)
    conn.close()

    return [row["Partner_Code"] for i, row in results.iterrows()]
