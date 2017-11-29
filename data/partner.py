import pandas as pd
from data import sdb_connect


def query_partner_data(**args):
    from schema.partner import PartnersAllocations, AllocatedTime

    sql = ' select * from  PeriodTimeDist ' \
          '    join Partner using(Partner_Id)  ' \
          '    join Semester using(Semester_Id)  '

    if args['semester'] is not None:
        sql = sql + ' where concat(Year,"-", Semester) = "{semester}"'.format(semester=args['semester'])

    if args['partner_code'] is not None:
        if "where" in sql:
            sql += " and Partner_Code = '{partner_code}'".format(partner_code=args['partner_code'])
        else:
            sql += " where Partner_Code = '{partner_code}'".format(partner_code=args['partner_code'])

    conn = sdb_connect()
    results = pd.read_sql(sql + " order by Partner_Code", conn)
    conn.close()
    partners, pc = [], []
    for index, row in results.iterrows():
        if row["Partner_Code"] not in pc:
            partners.append(PartnersAllocations(
                id="Partner: " + str(row["Partner_Id"]),
                name=row["Partner_Name"],
                code=row["Partner_Code"],
                allocated_time=[]

            ))
        partners[len(partners) - 1].allocated_time.append(
            AllocatedTime(
                for_semester=str(row['Year'])+"-"+str(row['Semester']),

                Allocated_p0_p1=row['Alloc0and1'],
                Allocated_p2=row['Alloc2'],
                Allocated_p3=row['Alloc3'],

                used_p0_p1=row['Used0and1'],
                used_p2=row['Used2'],
                used_p3=row['Used3']
            ))
        pc.append(row["Partner_Code"])


    return partners


def get_partners(**args):
    data = query_partner_data(**args)
    return data
