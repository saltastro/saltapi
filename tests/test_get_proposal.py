import json
import os

import pytest
from unittest.mock import patch, Mock


def test_get_proposal_successful(client):
    with patch('run.request') as mock_requests:
        mock_requests.get.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 200

        response = client.get('proposals/2018-2-SCI-040', query_string={'proposal_phase': 1})

        # Assert the response status code to be 200 for successful post request
        assert response.status_code == 200
        # Assert the response content type to be a zip when the proposal retrieved successfully
        assert response.headers['Content-Type'] == 'application/zip'


@pytest.mark.parametrize(('status_code', 'error_message',), (
    (401, {'error': 'Invalid credentials'},),
    (403, {'error': 'Have no permissions to make this request'},),
))
def test_get_proposal_forbidden_unauthorized(client, status_code, error_message):
    with patch('run.requests') as mock_requests:
        mock_requests.get.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = status_code

        mock_response.json.return_value = error_message

        response = client.get('proposals/proposal_code', query_string={'proposal_phase': 1})

        # Assert the response status code for a forbidden and unauthorized user trying to get a proposal
        assert response.status_code == status_code
        # Assert the response error message
        assert json.loads(response.data)['error'] == error_message['error']
        # Assert the response content type to be a json
        assert response.headers['Content-Type'] == 'application/json'


def test_get_proposal_not_found(client):
    with patch('run.requests') as mock_requests:
        mock_requests.get.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 404

        mock_response.json.return_value = {'error': 'Proposal not found '}

        response = client.get('proposals/proposal_code', query_string={'proposal_phase': 1})

        # Assert the response status code to be 400 for not found get request
        assert response.status_code == 404
        # Assert the response error message
        assert json.loads(response.data)['error'] == 'Proposal not found '
        # Assert the response content type to be a json when the proposal to be retrieved not found
        assert response.headers['Content-Type'] == 'application/json'


@pytest.mark.parametrize(('status_code',), (
        (405,),)
                         )
def test_submit_proposal_disallowed_request_methods(client, status_code):
    endpoint = 'proposals/proposal_code'
    # Assert the response status code to be 405 for not allowed request method when retrieving a proposal
    assert client.post(endpoint).status_code == status_code
    assert client.put(endpoint).status_code == status_code
    assert client.patch(endpoint).status_code == status_code
    assert client.delete(endpoint).status_code == status_code

    # Assert the response content type to be a json when the get response Not Allowed Method error message returned
    assert client.post(endpoint).headers['Content-Type'] == 'application/json'
    assert client.put(endpoint).headers['Content-Type'] == 'application/json'
    assert client.patch(endpoint).headers['Content-Type'] == 'application/json'
    assert client.delete(endpoint).headers['Content-Type'] == 'application/json'


def test_get_proposal_functionality(client):
    endpoint = 'proposals/proposal_code'
    with patch('run.requests.get') as mock_request:
        client.get(endpoint, query_string={'proposal_phase': 1})

        print(mock_request.call_args)

        # Assert a get request is called with a url
        # http://localhost/webmanager/replicates/proposals/proposal_code/1/proposal_code.zip
        assert mock_request.call_args[0][0] == os.environ.get('PROPOSALS_DIR') + '/proposal_code/1/proposal_code.zip'
