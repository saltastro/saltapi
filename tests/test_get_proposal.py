import json
import os
import pytest
from unittest.mock import patch, Mock


def test_get_proposal_with_phase_successful(client, auth_header):
    with patch('run.latest_version') as latest_version:
        latest_version.return_value = 1

        proposal_code = '2018-2-SCI-040'
        phase = 1

        response = client.get('/proposals/' + proposal_code, query_string={'proposal_phase': phase}, headers=auth_header)

        file_location = '{}{}/{}/{}.zip'.format(
            os.environ.get('PROPOSALS_DIR'),
            proposal_code,
            latest_version.return_value,
            proposal_code
        )

        with open(file_location, 'rb') as file:
            # assert the status code when the file is retrieved successfully
            assert response.status_code == 200
            # assert the content of the file retrieved to match the one of the exact file
            assert response.data == file.read()
            # assert the content type of the retrieved file
            assert response.headers['Content-Type'] == 'application/zip'
            # assert the disposition to have file name with proposal code
            assert proposal_code in response.headers['Content-Disposition']


@pytest.mark.parametrize(('proposal_code', 'proposal_phase',), (
    ('proposal_code', 1,),
    ('2018-2-SCI-040', 2,),
))
def test_get_proposal_with_phase_not_found(client, proposal_code, proposal_phase, auth_header):
    with patch('run.latest_version') as latest_version:
        latest_version.side_effect = Mock(side_effect=Exception('Proposal not found'))

        endpoint = '/proposals/' + proposal_code

        response = client.get(endpoint, query_string={'proposal_phase': proposal_phase}, headers=auth_header)

        # assert the status code when the proposal not found
        assert response.status_code == 404
        # assert the error message to contain 'proposal_code does not'
        assert 'not' in json.loads(response.data)['error']
        # assert the content type of the returned response
        assert response.headers['Content-Type'] == 'application/json'


def test_get_proposal_without_phase_successful(client, auth_header):
    with patch('run.latest_version') as latest_version:
        latest_version.return_value = 1

        proposal_code = '2018-2-SCI-040'

        response = client.get('/proposals/' + proposal_code, headers=auth_header)

        file_location = '{}{}/{}/{}.zip'.format(
            os.environ.get('PROPOSALS_DIR'),
            proposal_code,
            latest_version.return_value,
            proposal_code
        )

        with open(file_location, 'rb') as file:

            # assert the status code when the file is retrieved successfully
            assert response.status_code == 200
            # assert the content of the file retrieved to match the one of the exact file
            assert response.data == file.read()
            # assert the content type
            assert response.headers['Content-Type'] == 'application/zip'
            # assert the disposition to have file name with proposal code
            assert proposal_code in response.headers['Content-Disposition']


def test_get_proposal_without_phase_not_found(client, auth_header):
    with patch('run.latest_version') as latest_version:
        latest_version.side_effect = Mock(side_effect=Exception('Proposal not found'))

        endpoint = '/proposals/proposal_code'

        response = client.get(endpoint, headers=auth_header)

        # assert the status code when the proposal not found
        assert response.status_code == 404
        # assert the error message to contain 'proposal_code does not'
        assert 'not' in json.loads(response.data)['error']
        # assert the content type of the returned response
        assert response.headers['Content-Type'] == 'application/json'


def test_get_proposal_invalid_phase(client, auth_header):

    endpoint = '/proposals/proposal_code'

    response = client.get(endpoint, query_string={'proposal_phase': 5}, headers=auth_header)

    # assert the status code for a bad request
    assert response.status_code == 400
    # assert the error message for proposal_phase when invalid phase passed
    assert json.loads(response.data)['error'] == 'Bad request, only values 1 and 2 allowed for proposal_phase'
    # assert the content type of the returned response
    assert response.headers['Content-Type'] == 'application/json'


def test_get_proposal_unauthorized(client):
    response = client.get('/proposals/proposal_code')

    # assert the status code for an unauthorized user
    assert response.status_code == 401


def test_get_proposal_disallowed_request_methods(client, auth_header):
    endpoint = '/proposals/proposal_code'
    # Assert the response status code for not allowed request method
    assert client.put(endpoint, headers=auth_header).status_code == 405
    assert client.post(endpoint, headers=auth_header).status_code == 405
    assert client.delete(endpoint, headers=auth_header).status_code == 405

    # Assert the response content type
    assert client.put(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
    assert client.post(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
    assert client.delete(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
