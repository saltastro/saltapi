import pandas as pd
from data import sdb_connect
import pytest
import numpy as np


def get_bock_visit_status_id(observation_status):
    sql = '''SELECT BlockVisitStatus_Id FROM BlockVisitStatus
WHERE BlockVisitStatus.BlockVisitStatus = %s
'''
    df = pd.read_sql(sql, params=(observation_status,), con=sdb_connect())

    return df['BlockVisitStatus_Id'][0] or 0


def get_semester_id(semester):
    year = semester.split('-')[0]
    year_semester = semester.split('-')[1]
    sql = '''SELECT Semester_Id FROM Semester
WHERE Semester.Year = %s
AND Semester.Semester = %s'''
    df = pd.read_sql(sql, params=(year, year_semester,), con=sdb_connect())

    return df['Semester_Id'][0] or 0


def get_proposal_code_id(proposal_code):
    sql = '''SELECT ProposalCode_Id FROM ProposalCode
WHERE ProposalCode.Proposal_Code = %s'''
    df = pd.read_sql(sql, params=(proposal_code,), con=sdb_connect())

    return df['ProposalCode_Id'][0] or 0


def observation_completeness(proposal_code_id, semester_id, blocks_status_id, priority):

    sql = '''SELECT sum(ObsTime) AS Total_Observed FROM BlockVisit
JOIN Block USING (Block_Id)
JOIN Proposal USING (Proposal_Id)
WHERE Proposal.ProposalCode_Id = %s
AND Semester_Id = %s
AND BlockVisitStatus_Id = %s
AND Priority = %s'''
    df = pd.read_sql(sql, params=(proposal_code_id, semester_id, blocks_status_id, priority,), con=sdb_connect())

    return df['Total_Observed'][0] or 0


def total_time_allocation(proposal_code_id, semester_id, priority):
    sql = '''SELECT sum(TimeAlloc) AS Total_Alloc_Time FROM MultiPartner 
JOIN PriorityAlloc using(MultiPartner_Id)
WHERE ProposalCode_Id = %s 
AND Semester_Id = %s 
AND Priority = %s'''
    df = pd.read_sql(sql, params=(proposal_code_id, semester_id, priority,), con=sdb_connect())

    return df['Total_Alloc_Time'][0] or 0


def completeness_percentage(proposal_code, semester, observation_status, priority):
    proposal_code_id = np.int64(get_proposal_code_id(proposal_code)).item()
    semester_id = np.int64(get_semester_id(semester)).item()
    blocks_status_id = np.int64(get_bock_visit_status_id(observation_status)).item()
    observed = np.int64(observation_completeness(proposal_code_id, semester_id, blocks_status_id, priority)).item()
    allocated = np.int64(total_time_allocation(proposal_code_id, semester_id, priority)).item()
    if allocated == 0:
        return 0
    percentage = (observed / allocated) * 100
    return percentage


semester = '2018-2'
status = 'ACCEPTED'
priority = [0, 1, 2, 3, 4]
proposal = [
    '2015-2-MLT-006', '2017-1-MLT-003', '2017-1-MLT-004', '2017-1-MLT-012', '2017-2-MLT-001', '2017-2-MLT-003',
    '2017-2-MLT-004', '2017-2-SCI-052', '2018-1-MLT-001', '2018-1-MLT-002', '2018-1-MLT-003', '2018-1-MLT-004',
    '2018-1-MLT-005', '2018-1-MLT-006', '2018-1-MLT-007', '2018-1-MLT-008', '2018-1-MLT-009', '2018-1-MLT-012',
    '2018-1-MLT-014', '2018-1-SCI-011', '2018-1-SCI-012', '2018-1-SCI-029', '2018-1-SCI-041', '2018-1-SCI-046',
    '2018-2-LSP-001', '2018-2-MLT-001', '2018-2-MLT-002', '2018-2-MLT-003', '2018-2-MLT-004', '2018-2-MLT-005',
    '2018-2-MLT-006', '2018-2-MLT-007',

]


@pytest.mark.parametrize(('proposal_code', 'semester', 'observation_status', 'priority', 'result',), (
    # input and expected values for the proposal 2015-2-MLT-006
    (proposal[0], semester, status, priority[0], 0,), (proposal[0], semester, status, priority[1], 81.55,),
    (proposal[0], semester, status, priority[2], 5.06,), (proposal[0], semester, status, priority[3], 0,),
    (proposal[0], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2017-1-MLT-003
    (proposal[1], semester, status, priority[0], 0,), (proposal[1], semester, status, priority[1], 27.12,),
    (proposal[1], semester, status, priority[2], 0,), (proposal[1], semester, status, priority[3], 0,),
    (proposal[1], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2017-1-MLT-004
    (proposal[2], semester, status, priority[0], 0,), (proposal[2], semester, status, priority[1], 0,),
    (proposal[2], semester, status, priority[2], 0,), (proposal[2], semester, status, priority[3], 31.08,),
    (proposal[2], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2017-1-MLT-012
    (proposal[3], semester, status, priority[0], 0,), (proposal[3], semester, status, priority[1], 0,),
    (proposal[3], semester, status, priority[2], 0,), (proposal[3], semester, status, priority[3], 4.65,),
    (proposal[3], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2017-2-MLT-001
    (proposal[4], semester, status, priority[0], 0,), (proposal[4], semester, status, priority[1], 44.86,),
    (proposal[4], semester, status, priority[2], 18.43,), (proposal[4], semester, status, priority[3], 0,),
    (proposal[4], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2017-2-MLT-003
    (proposal[5], semester, status, priority[0], 0,), (proposal[5], semester, status, priority[1], 0,),
    (proposal[5], semester, status, priority[2], 0,), (proposal[5], semester, status, priority[3], 0,),
    (proposal[5], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2017-2-MLT-004
    (proposal[6], semester, status, priority[0], 0,), (proposal[6], semester, status, priority[1], 0,),
    (proposal[6], semester, status, priority[2], 0,), (proposal[6], semester, status, priority[3], 0,),
    (proposal[6], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2017-2-MLT-004
    (proposal[7], semester, status, priority[0], 0,), (proposal[7], semester, status, priority[1], 19.67,),
    (proposal[7], semester, status, priority[2], 0,), (proposal[7], semester, status, priority[3], 0,),
    (proposal[7], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-001
    (proposal[8], semester, status, priority[0], 0,), (proposal[8], semester, status, priority[1], 0,),
    (proposal[8], semester, status, priority[2], 0,), (proposal[8], semester, status, priority[3], 0,),
    (proposal[8], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-002
    (proposal[9], semester, status, priority[0], 0,), (proposal[9], semester, status, priority[1], 0,),
    (proposal[9], semester, status, priority[2], 0,), (proposal[9], semester, status, priority[3], 0,),
    (proposal[9], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-003
    (proposal[10], semester, status, priority[0], 0,), (proposal[10], semester, status, priority[1], 0,),
    (proposal[10], semester, status, priority[2], 67.24,), (proposal[10], semester, status, priority[3], 0,),
    (proposal[10], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-004
    (proposal[11], semester, status, priority[0], 0,), (proposal[11], semester, status, priority[1], 11.10,),
    (proposal[11], semester, status, priority[2], 0,), (proposal[11], semester, status, priority[3], 0,),
    (proposal[11], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-005
    (proposal[12], semester, status, priority[0], 0,), (proposal[12], semester, status, priority[1], 33.22,),
    (proposal[12], semester, status, priority[2], 50.51,), (proposal[12], semester, status, priority[3], 0,),
    (proposal[12], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-006
    (proposal[13], semester, status, priority[0], 23.81,), (proposal[13], semester, status, priority[1], 0,),
    (proposal[13], semester, status, priority[2], 8.33,), (proposal[13], semester, status, priority[3], 0,),
    (proposal[13], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-007
    (proposal[14], semester, status, priority[0], 0,), (proposal[14], semester, status, priority[1], 42.85,),
    (proposal[14], semester, status, priority[2], 24.99,), (proposal[14], semester, status, priority[3], 0,),
    (proposal[14], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-008
    (proposal[15], semester, status, priority[0], 0,), (proposal[15], semester, status, priority[1], 0,),
    (proposal[15], semester, status, priority[2], 0,), (proposal[15], semester, status, priority[3], 4.61,),
    (proposal[15], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-009
    (proposal[16], semester, status, priority[0], 0,), (proposal[16], semester, status, priority[1], 0,),
    (proposal[16], semester, status, priority[2], 0,), (proposal[16], semester, status, priority[3], 1.21),
    (proposal[16], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-012
    (proposal[17], semester, status, priority[0], 49.56,), (proposal[17], semester, status, priority[1], 49.50,),
    (proposal[17], semester, status, priority[2], 0,), (proposal[17], semester, status, priority[3], 0),
    (proposal[17], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-MLT-014
    (proposal[18], semester, status, priority[0], 0,), (proposal[18], semester, status, priority[1], 23.67,),
    (proposal[18], semester, status, priority[2], 0,), (proposal[18], semester, status, priority[3], 0),
    (proposal[18], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-SCI-011
    (proposal[19], semester, status, priority[0], 0,), (proposal[19], semester, status, priority[1], 0,),
    (proposal[19], semester, status, priority[2], 0,), (proposal[19], semester, status, priority[3], 0),
    (proposal[19], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-SCI-012
    (proposal[20], semester, status, priority[0], 0,), (proposal[20], semester, status, priority[1], 0,),
    (proposal[20], semester, status, priority[2], 0,), (proposal[20], semester, status, priority[3], 0),
    (proposal[20], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-SCI-029
    (proposal[21], semester, status, priority[0], 0,), (proposal[21], semester, status, priority[1], 0,),
    (proposal[21], semester, status, priority[2], 0,), (proposal[21], semester, status, priority[3], 92.08),
    (proposal[21], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-SCI-041
    (proposal[22], semester, status, priority[0], 0,), (proposal[22], semester, status, priority[1], 0,),
    (proposal[22], semester, status, priority[2], 0,), (proposal[22], semester, status, priority[3], 0),
    (proposal[22], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-1-SCI-046
    (proposal[23], semester, status, priority[0], 0,), (proposal[23], semester, status, priority[1], 0,),
    (proposal[23], semester, status, priority[2], 0,), (proposal[23], semester, status, priority[3], 0),
    (proposal[23], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-LSP-001
    (proposal[24], semester, status, priority[0], 19.00,), (proposal[24], semester, status, priority[1], 10.42,),
    (proposal[24], semester, status, priority[2], 22.43,), (proposal[24], semester, status, priority[3], 0),
    (proposal[24], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-MLT-001
    (proposal[25], semester, status, priority[0], 0,), (proposal[25], semester, status, priority[1], 0,),
    (proposal[25], semester, status, priority[2], 100.30,), (proposal[25], semester, status, priority[3], 0),
    (proposal[25], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-MLT-002
    (proposal[26], semester, status, priority[0], 0,), (proposal[26], semester, status, priority[1], 0,),
    (proposal[26], semester, status, priority[2], 0,), (proposal[26], semester, status, priority[3], 0),
    (proposal[26], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-MLT-003
    (proposal[27], semester, status, priority[0], 0,), (proposal[27], semester, status, priority[1], 50.01,),
    (proposal[27], semester, status, priority[2], 99.98,), (proposal[27], semester, status, priority[3], 0),
    (proposal[27], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-MLT-004
    (proposal[28], semester, status, priority[0], 0,), (proposal[28], semester, status, priority[1], 0,),
    (proposal[28], semester, status, priority[2], 0,), (proposal[28], semester, status, priority[3], 3.27),
    (proposal[28], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-MLT-005
    (proposal[29], semester, status, priority[0], 0,), (proposal[29], semester, status, priority[1], 0,),
    (proposal[29], semester, status, priority[2], 7.66,), (proposal[29], semester, status, priority[3], 0),
    (proposal[29], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-MLT-006
    (proposal[30], semester, status, priority[0], 0,), (proposal[30], semester, status, priority[1], 0,),
    (proposal[30], semester, status, priority[2], 18.11,), (proposal[30], semester, status, priority[3], 0),
    (proposal[30], semester, status, priority[4], 0,),
    # input and expected values for the proposal 2018-2-MLT-007
    (proposal[31], semester, status, priority[0], 0,), (proposal[31], semester, status, priority[1], 0,),
    (proposal[31], semester, status, priority[2], 0,), (proposal[31], semester, status, priority[3], 2.69),
    (proposal[31], semester, status, priority[4], 0,),
))
def test_observation_completeness(proposal_code, semester, observation_status, priority, result):
    # assert the completeness percentage of the specified proposal code
    # for the specified semester, observation status and the priority of the observation
    assert round(completeness_percentage(proposal_code, semester, observation_status, priority), 2) == result
