import pandas as pd
from logging import log
from data import sdb_connect
import datetime
import warnings
from dateutil.relativedelta import relativedelta

semester_data = {}


class Semester:
    id = None
    semester = None
    start_semester = None
    end_semester = None

    @staticmethod
    def get_semester(active=False, semester_code=None):
        """
        :return:
        """
        sql = 'SELECT  Semester_Id, CONCAT(Year,"_", Semester) as SemesterCode, StartSemester, EndSemester ' \
              ' FROM  Semester '

        date = datetime.datetime.now().date()
        date_3 = date + relativedelta(months=3)

        if active:
            if not pd.isnull(semester_code):
                warnings.warn("Semester id or Semester code is provided and active=True, active semester is returned. "
                              "Set active=False if you need none active semester if you query for none active semester."
                              "Returned is active Semester")

            sql = sql + ' where StartSemester <= "{date_}" and "{date_}" < EndSemester;'.format(date_=date_3)
        else:
            try:
                if not pd.isnull(semester_code):
                    int(semester_code[:4])
                    int(semester_code[5:])
                    if "_" in semester_code:
                        semester_code = semester_code.replace("_", "-")
                    if len(semester_code) != 6:
                        raise ValueError("{semester_code} is not a semester".format(semester_code=semester_code))

                    sql = sql + ' WHERE (CONCAT(Year, "-", Semester) = "{semester_code}") ' \
                        .format(semester_code=semester_code)
                else:
                    raise ValueError(
                        "Set active=True for active semester, or provide semester_id or semester like '2017_1'  "
                        "or '2017-1'")
            except ValueError:
                return None
        conn = sdb_connect()
        try:
            data = pd.read_sql(sql, conn)
            conn.close()
            return [Semester().__make_semester(data=s) for i, s in data.iterrows()][0]
        except Exception as err:
            log(1, err)
            raise RuntimeError("Failed to get semester data")

    def __make_semester(self, data):
        # Todo This method is called only by get semester it is suppose to be a private method for semester
        """
         make a data received a
        :param data:
        :return:
        """
        self.id = data['Semester_Id']
        self.semester = data['SemesterCode']
        self.start_semester = data['StartSemester']
        self.end_semester = data['EndSemester']
        return self
