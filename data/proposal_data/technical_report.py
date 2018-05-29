import pandas as pd
from data import sdb_connect


def get_technical_reports(proposal_code_ids):
    technical_reports = {}
    tech_report_sql = """
        SELECT  ProposalCode.Proposal_Code as Proposal_Code,
               CONCAT(Semester.Year, '-', Semester.Semester) AS Semester,
               FirstName, Surname, Email, Username,
               TechReport, ProposalCode.ProposalCode_Id as ProposalCode_Id
        FROM ProposalTechReport
             JOIN ProposalCode ON ProposalTechReport.ProposalCode_Id = ProposalCode.ProposalCode_Id
             JOIN Semester ON ProposalTechReport.Semester_Id = Semester.Semester_Id
             LEFT JOIN Investigator ON ProposalTechReport.Astronomer_Id=Investigator.Investigator_Id
             LEFT JOIN PiptUser ON Investigator.PiptUser_Id=PiptUser.PiptUser_Id
        WHERE ProposalCode.ProposalCode_Id IN {proposal_code_ids}
        ORDER BY Semester.Year ASC, Semester.Semester ASC
        """.format(proposal_code_ids=proposal_code_ids)
    conn = sdb_connect()
    for index, row in pd.read_sql(tech_report_sql, conn).iterrows():
        proposal_code = row['Proposal_Code']
        if proposal_code not in technical_reports:
            technical_reports[proposal_code] = []
        technical_reports[proposal_code].append(
            dict(Semester=row['Semester'],
                 ReviewerFirstName=row['FirstName'],
                 ReviewerLastName=row['Surname'],
                 ReviewerEmail=row['Email'],
                 ReviewerUsername=row['Username'],
                 Report=row['TechReport'])
        )
    conn.close()
    print(technical_reports)
    return technical_reports
