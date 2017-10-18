import graphene as g
from graphene import relay as r
import pandas as pd
from data import conn

import datetime
import warnings
from dateutil.relativedelta import relativedelta


class Semester(g.ObjectType):

    semester_id = g.Int()
    semester = g.String()
    start_semester = g.String()
    end_semester = g.String()

    @staticmethod
    def get_semester(id_only=False, active=False, semester_code=None, all_data=False):
        """
        :return:
        """
        sql = 'SELECT  Semester_Id, CONCAT(Year,"_", Semester) as SemesterCode, StartSemester, EndSemester ' \
              ' FROM  Semester '

        if all_data:
            data = pd.read_sql(sql, conn)

            li = [Semester.__make_semester(d) for i, d in data.iterrows()]
            return li

        date = datetime.datetime.now().date()
        date_3 = date + relativedelta(months=3)

        if active:
            if not pd.isnull(semester_code):
                warnings.warn("Semester id or Semester code is provided and active=True, active semester is returned. "
                              "Set active=False if you need none active semester if you query for none active semester."
                              "Returned is active Semester")

            sql = sql + ' where StartSemester <= "{date_}" and "{date_}" < EndSemester;'.format(date_=date_3)
        else:
            if not pd.isnull(semester_code):

                sql = sql + ' WHERE (CONCAT(Year, "-", Semester) = "{semester_code}" ' \
                            '   OR CONCAT(Year, "_", Semester) = "{semester_code}") '\
                    .format(semester_code=semester_code)
            else:
                raise ValueError(
                    "Set active=True for active semester, or provide semester_id or semester like '2017_1'  "
                    "or '2017-1'")

        data = pd.read_sql(sql, conn)
        try:
            semester = [Semester.__make_semester(s) for i, s in data.iterrows()][0]
        except IndexError:
            semester = None

        if id_only:
            return None if pd.isnull(semester) else semester.semester_id
        return semester

    @staticmethod
    def __make_semester(data):
        # Todo This method is called only by get semester it is suppose to be a private method for semester
        """
         make a data received a
        :param data:
        :return:
        """
        semest = Semester()
        semest.semester_id = data['Semester_Id']
        semest.semester = data['SemesterCode']
        semest.start_semester = data['StartSemester']
        semest.end_semester = data['EndSemester']
        return semest


class UserRole(g.Enum):
    VISITOR = 1
    INVESTIGATOR = 2
    TAC_MEMBER = 3
    TAC_CHAIR = 4
    SALT_ASTRONOMER = 5
    ADMINISTRATOR = 6


class Person(g.ObjectType):
    class Meta:
        interfaces = (r.Node,)

    user_id = g.ID()
    surname = g.String()
    first_name = g.String()
    email = g.String()
    # roles = graphene.Field(UserRole, description="A user role object")  # ** was a list **
    pipt_user_id = g.Int()
    phone = g.String()
    institute_id = g.Int()


class ObservingConditions(g.ObjectType):
    class Meta:
        interfaces = (r.Node,)

    max_seeing = g.Float()
    transparency = g.String() # be enum
    description = g.String()


class Thesis(g.ObjectType): # was p1thesis
    class Meta:
        interfaces = (r.Node,)
    thesis_type = g.String()  # be Enum
    thesis_description = g.String()
    student = g.Field(Person)
    # todo add year of completion



