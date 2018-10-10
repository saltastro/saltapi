import json
import os
from unittest.mock import patch, Mock
from .tests_util import create_zipfile, create_non_zipfile


def test_replace_proposal_successful(client, auth_header):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()

        # setting the mock response
        mock_response.status_code = 200

        proposal_code = "2018-2-SCI-040"

        endpoint = 'proposals/' + proposal_code

        response = client.patch(endpoint, data=create_zipfile(), headers=auth_header)

        # Assert the response status code for successful proposal modification
        assert response.status_code == 204


def test_replace_proposal_unauthorized(client):
    response = client.patch('proposals/proposal_code', data=create_zipfile())

    # Assert the response status code for an unauthorized user
    assert response.status_code == 401


def test_replace_proposal_without_file_response(client, auth_header):
    response = client.patch('proposals/2018-2-SCI-040', headers=auth_header)

    # Assert the response status code for bad request
    assert response.status_code == 400
    # Assert the response error message when trying to replace with file unattached
    assert json.loads(response.data)['error'] == 'No file is attached'
    # Assert the response content type
    assert response.headers['Content-Type'] == 'application/json'


def test_replace_proposal_unsupported_media_type(client, auth_header):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 415

        mock_response.json.return_value = {'Error': 'Only zip file is supported'}

        response = client.patch('proposals/2018-2-SCI-040', data=create_non_zipfile(), headers=auth_header)

        # Assert the response status code to be 415 for unsupported media type
        assert response.status_code == 415
        # Assert the response error message to be Only zip file is supported when other format tried to be used
        assert json.loads(response.data)['error'] == 'Only zip file is supported'
        # Assert the response content type
        assert response.headers['Content-Type'] == 'application/json'


def test_replace_proposal_not_found(client, auth_header):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 404

        mock_response.json.return_value = {'Error': 'Proposal not found '}

        response = client.patch('proposals/proposal_code', data=create_zipfile(), headers=auth_header)

        # Assert the response status code to be 400 for not found get request
        assert response.status_code == 404
        # Assert the response error message
        assert json.loads(response.data)['error'] == 'Proposal not found '
        # Assert the response content type
        assert response.headers['Content-Type'] == 'application/json'


def test_replace_proposal_disallowed_request_methods(client, auth_header):
    endpoint = '/proposals/proposal_code'
    # Assert the response status code for not allowed request method
    assert client.put(endpoint, headers=auth_header).status_code == 405
    assert client.post(endpoint, headers=auth_header).status_code == 405
    assert client.delete(endpoint, headers=auth_header).status_code == 405

    # Assert the response content type
    assert client.put(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
    assert client.post(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
    assert client.delete(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'


def test_get_proposal_functionality(client, auth_header):
    with patch('run.requests.post') as mock_request:
        mock_request.return_value = mock_response = Mock()
        mock_response.status_code = 'For testing'
        mock_response.json.return_value = {'Error': 'For test '}
        endpoint = 'proposals/proposal_code'

        client.patch(endpoint, data=create_zipfile(), headers=auth_header)

        # Assert a post request is called with a correct url
        assert mock_request.call_args[0][0] == os.environ.get('WM_WEB_SERVICES')

        # Assert the proposal file content
        assert mock_request.call_args[1]['files']['proposal_content'].read() == create_zipfile()

