import json
import os
from unittest.mock import patch, Mock
from .tests_util import create_zipfile, create_non_zipfile

ENDPOINT = '/proposals'
TOKEN = os.environ.get('TOKEN')


def test_submit_proposal_successful(client, uri):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 200

        new_proposal_code = "new_proposal_code"

        mock_response.json.return_value = {"Proposal_Code": new_proposal_code}

        headers = {'Authorization': 'token ' + TOKEN}

        response = client.post(ENDPOINT, data=create_zipfile(), headers=headers)

        # Assert the response status code for successful post request
        assert response.status_code == 200
        # Assert the response data for the proposal_code when the proposal submitted successful
        assert json.loads(response.data)['proposal_code'] == new_proposal_code
        # Assert the response content type to be a json
        assert response.headers['Content-Type'] == 'application/json'
        # Assert the response headers location is correct
        assert response.headers['Location'] == uri('/proposals/' + new_proposal_code)


def test_submit_proposal_without_file_response(client):
    headers = {'Authorization': 'token ' + TOKEN}

    response = client.post(ENDPOINT, headers=headers)

    # Assert the response status code for bad request
    assert response.status_code == 400
    # Assert the response error message when file is not attached
    assert json.loads(response.data)['error'] == 'No file is attached'
    # Assert the response content type
    assert response.headers['Content-Type'] == 'application/json'


def test_submit_proposal_unsupported_media_type(client):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 415

        mock_response.json.return_value = {'Error': 'Only zip file is supported'}

        headers = {'Authorization': 'token ' + TOKEN}

        response = client.post(ENDPOINT, data=create_non_zipfile(), headers=headers)

        # Assert the response status code for unsupported media type
        assert response.status_code == 415
        # Assert the response error message when other format tried to be submitted
        assert json.loads(response.data)['error'] == 'Only zip file is supported'
        # Assert the response content type
        assert response.headers['Content-Type'] == 'application/json'


def test_submit_proposal_unauthorized(client):
    response = client.post(ENDPOINT, data=create_zipfile())

    # Assert the response status code for an unauthorized user
    assert response.status_code == 401


def test_submit_proposal_disallowed_request_methods(client):
    # Assert the response status code for not allowed request method
    assert client.get(ENDPOINT).status_code == 405
    assert client.put(ENDPOINT).status_code == 405
    assert client.patch(ENDPOINT).status_code == 405
    assert client.delete(ENDPOINT).status_code == 405

    # Assert the response content type
    assert client.get(ENDPOINT).headers['Content-Type'] == 'application/json'
    assert client.put(ENDPOINT).headers['Content-Type'] == 'application/json'
    assert client.patch(ENDPOINT).headers['Content-Type'] == 'application/json'
    assert client.delete(ENDPOINT).headers['Content-Type'] == 'application/json'


def test_submit_proposal_functionality(client):
    with patch('run.requests.post') as mock_request:
        mock_request.return_value = mock_response = Mock()
        mock_response.status_code = 'For testing'
        mock_response.json.return_value = {'Error': 'For test '}

        headers = {'Authorization': 'token ' + TOKEN}

        client.post(ENDPOINT, data=create_zipfile(), headers=headers)

        # Assert a post request is called with a correct url
        assert mock_request.call_args[0][0] == os.environ.get('WM_WEB_SERVICES')

        # Assert the proposal file content
        assert mock_request.call_args[1]['files']['proposal_content'].read() == create_zipfile()
