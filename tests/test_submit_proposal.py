import json
import os
from io import BytesIO
from unittest.mock import patch, Mock
import zipfile
import pytest

ENDPOINT = '/proposals'


# Creating a zip file
def create_zipfile():
    proposal_content = BytesIO()
    with zipfile.ZipFile(proposal_content, 'w') as zip_file:
        zip_file.writestr('content', b'proposal content')

    proposal_content.seek(0)

    return proposal_content.read()


# Creating a non zip file
def create_non_zipfile():
    file_content = BytesIO(b'any file content')

    return file_content.read()


def test_submit_proposal_successful(client, uri):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 200

        new_proposal_code = "new_proposal_code"

        mock_response.json.return_value = {"Proposal_Code": new_proposal_code}

        response = client.post(ENDPOINT, data=create_zipfile())

        # Assert the response status code to be 200 for successful post request
        assert response.status_code == 200
        # Assert the response data for the proposal_code to be new_proposal_code when the proposal submitted successful
        assert json.loads(response.data)['proposal_code'] == new_proposal_code
        # Assert the response content type to be a json when the proposal submitted successful
        assert response.headers['Content-Type'] == 'application/json'
        # Assert the response headers location to be
        # /proposals/proposal_code when the proposal submitted successful
        assert response.headers['Location'] == uri('/proposals/' + new_proposal_code)


def test_submit_proposal_without_file_response(client):
    response = client.post(ENDPOINT)

    # Assert the response status code to be 400 for bad request
    assert response.status_code == 400
    # Assert the response error message to be No file is attached when trying to submit with file unattached
    assert json.loads(response.data)['error'] == 'No file is attached'
    # Assert the response content type to be a json when the post response unsupported type error message returned
    assert response.headers['Content-Type'] == 'application/json'


def test_submit_proposal_unsupported_media_type(client):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = 415

        mock_response.json.return_value = {'Error': 'Only zip file is supported'}

        response = client.post(ENDPOINT, data=create_non_zipfile())

        # Assert the response status code to be 415 for unsupported media type
        assert response.status_code == 415
        # Assert the response error message to be Only zip file is supported when other format tried to be submitted
        assert json.loads(response.data)['error'] == 'Only zip file is supported'
        # Assert the response content type to be a json when the post response unsupported type error message returned
        assert response.headers['Content-Type'] == 'application/json'


@pytest.mark.parametrize(('status_code', 'error_message',), (
        (403, {'Error': 'Have no permissions to make this request'},),
        (401, {'Error': 'Invalid credentials'},),)
                         )
def test_submit_proposal_forbidden_unauthorized(client, status_code, error_message):
    with patch('run.requests') as mock_requests:
        mock_requests.post.return_value = mock_response = Mock()
        # setting the mock response
        mock_response.status_code = status_code

        mock_response.json.return_value = error_message

        response = client.post(ENDPOINT, data=create_zipfile())

        # Assert the response status code for a forbidden and unauthorized user trying to submit a proposal
        assert response.status_code == status_code
        # Assert the response error message
        assert json.loads(response.data)['error'] == error_message['Error']
        # Assert the response content type to be a json
        assert response.headers['Content-Type'] == 'application/json'


@pytest.mark.parametrize(('status_code',), (
        (405,),)
                         )
def test_submit_proposal_disallowed_request_methods(client, status_code):
    # Assert the response status code to be 405 for not allowed request method when submitting a proposal
    assert client.get(ENDPOINT).status_code == status_code
    assert client.put(ENDPOINT).status_code == status_code
    assert client.patch(ENDPOINT).status_code == status_code
    assert client.delete(ENDPOINT).status_code == status_code

    # Assert the response content type to be a json when the post response Not Allowed Method error message returned
    assert client.get(ENDPOINT).headers['Content-Type'] == 'application/json'
    assert client.put(ENDPOINT).headers['Content-Type'] == 'application/json'
    assert client.patch(ENDPOINT).headers['Content-Type'] == 'application/json'
    assert client.delete(ENDPOINT).headers['Content-Type'] == 'application/json'


def test_submit_proposal_functionality(client):
    with patch('run.requests.post') as mock_request:
        client.post(ENDPOINT, data=create_zipfile())

        # Assert a post request is called with a url http://localhost/webservices/index.php
        assert mock_request.call_args[0][0] == os.environ.get('WM_WEB_SERVICES')

        # Assert the proposal file content
        assert mock_request.call_args[1]['files']['proposal_content'].read() == create_zipfile()
