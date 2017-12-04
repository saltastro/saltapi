import pandas as pd
from data import sdb_connect


def get_partners(semester, partner):
    from schema.partner import PartnerAllocations, AllocatedTime

    sql = ' select * from  PeriodTimeDist ' \
          '    join Partner using(Partner_Id)  ' \
          '    join Semester using(Semester_Id)  ' \
          ' where concat(Year,"-", Semester) = "{semester}" ' \
          ' and Partner_Code = "{partner_code}" ' \
          ' '.format(semester=semester, partner_code=partner)

    conn = sdb_connect()
    results = pd.read_sql(sql, conn)
    conn.close()
    partner = PartnerAllocations()
    for index, row in results.iterrows():
            partner.id = "Partner: " + str(row["Partner_Id"]),
            partner.name = row["Partner_Name"],
            partner.code = row["Partner_Code"],
            partner.allocated_time = AllocatedTime(
                for_semester=str(row['Year'])+"-"+str(row['Semester']),

                Allocated_p0_p1=row['Alloc0and1'],
                Allocated_p2=row['Alloc2'],
                Allocated_p3=row['Alloc3'],

                used_p0_p1=row['Used0and1'],
                used_p2=row['Used2'],
                used_p3=row['Used3']
            )

    return partner

