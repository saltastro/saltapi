from io import BytesIO
import json
from unittest.mock import MagicMock


def test_successful_submit_proposal_response(monkeypatch, client):
    # Creating the mocking substitute function for the post request/response to submitting proposal
    def mock_submit_proposal_post_request_response(*args, **kwargs):
        # setting up the response content
        return {
            'body': {
                'proposal-code': 'new_proposal_code'
            },
            'headers': {
                'Content-Type': 'application/json',
                'Location': 'wmdev.saao.ac.za/wm/proposals/new_proposal_code'
            }
        }

    # Mocking the post request/response to submitting proposal
    monkeypatch.setattr('run.requests.post', mock_submit_proposal_post_request_response)

    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.zip')

    response = client.post(endpoint, data={'file': file})

    resp = json.loads(response.data)

    # Assert the response status code to be 200 for successful request post
    assert response.status_code == 200

    # Assert the response content type to be a json when proposal submitted successful
    assert resp['headers']['Content-Type'] == "application/json"

    # Assert the response headers location to be http://proposals/new_proposal_code when proposal submitted successful
    assert resp['headers']['Location'] == 'wmdev.saao.ac.za/wm/proposals/new_proposal_code'

    # Assert the response data to be new_proposal_code when proposal submitted successful
    assert resp['body']['proposal-code'] == 'new_proposal_code'


def test_unsuccessful_submit_proposal_response(monkeypatch, client):
    """
    Test for the BAD REQUEST response status
    """

    # Creating the mocking substitute function for the post request/response to submitting proposal
    def mock_submit_proposal_post_response_bad(*args, **kwargs):
        # setting up the response content
        return {
            'status': '400 BAD REQUEST',
            'status_code': 400
        }

    # Mocking the post request/response to submitting proposal
    monkeypatch.setattr('run.requests.post', mock_submit_proposal_post_response_bad)

    endpoint = '/proposals'
    files = [(BytesIO(b'Proposal Content'), 'proposal.zip'), (BytesIO(b'Proposal Content'), 'proposal1.zip')]

    response = client.post(endpoint, data={'file': files})

    resp = json.loads(response.data)

    # Assert that the response returned a 400 status code if more than one file submitted
    assert resp['status_code'] == 400

    """
    End of test for the BAD REQUEST response status
    """

    """
    Test for the UNSUPPORTED MEDIA TYPE response status
    """

    # Creating the mocking substitute function for the post request/response to submitting proposal
    def mock_submit_proposal_post_response_media(*args, **kwargs):
        # setting up the response content
        return {
            'status': '415 UNSUPPORTED MEDIA TYPE',
            'status_code': 415
        }

    # Mocking the post request/response to submitting proposal
    monkeypatch.setattr('run.requests.post', mock_submit_proposal_post_response_media)

    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.text')

    response = client.post(endpoint, data={'file': file})

    resp = json.loads(response.data)

    # Assert that the response returned a 415 status_code if file type is not supported
    assert resp['status_code'] == 415

    """
    End of test for the UNSUPPORTED MEDIA TYPE response status
    """

    """
    Test for the UNAUTHORIZED response status
    """

    # Creating the mocking substitute function for the post request/response to submitting proposal
    def mock_submit_proposal_post_response_authentication(*args, **kwargs):
        # setting up the response content
        return {
            'status': '401 UNAUTHORIZED',
            'status_code': 401,
            'headers': {
                'Authentication': 'not authenticated'
            }
        }

    # Mocking the post request/response to submitting proposal
    monkeypatch.setattr('run.requests.post', mock_submit_proposal_post_response_authentication)

    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.zip')

    response = client.post(endpoint, data={'file': file})

    resp = json.loads(response.data)

    # Assert that the response returned an 401 status code if the user is not authenticated
    assert resp['status_code'] == 401

    """
    End of test for the UNAUTHORIZED response status
    """

    """
    Test for the FORBIDDEN response status
    """

    # Creating the mocking substitute function for the post request/response to submitting proposal
    def mock_submit_proposal_post_response_permission(*args, **kwargs):
        # setting up the response content
        return {
            'status': '403 FORBIDDEN',
            'status_code': 403,
            'headers': {
                'Authentication': 'not authorized'
            }
        }

    # Mocking the post request/response to submitting proposal
    monkeypatch.setattr('run.requests.post', mock_submit_proposal_post_response_permission)

    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.zip')

    response = client.post(endpoint, data={'file': file})

    resp = json.loads(response.data)

    # Assert that the response returned a 403 status code if the user is not authorized
    assert resp['status_code'] == 403

    """
    End of test for the FORBIDDEN response status
    """


def test_submit_proposal_disallowed_request_method(client):
    endpoint = '/proposals'

    response = client.get(endpoint)

    # Assert that the get request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(endpoint)

    # Assert that the put request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.delete(endpoint)

    # Assert that the delete request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.patch(endpoint)

    # Assert that the patch request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'


def test_submit_proposal_functionality(self, client):
    import run

    """
    Test for the file content
    """

    self.file_content = None

    # Creating the mocking substitute function for the post request/response to submitting proposal to get file content
    def mocked_file_content(*args, **kwargs):
        self.file_content = kwargs['data'].read()

    run.requests.post = mocked_file_content

    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.zip')
    client.post(endpoint, data={'file': file})

    # Assert the proposal file content to be b'Proposal Content'
    assert self.file_content == b'Proposal Content'

    """
    End of test for the file content
    """

    """
    Test for the post request arguments
    """

    # Mocking the post request method using the MagicMock class for the post request/response to submitting proposal
    run.requests.post = MagicMock()

    file = (BytesIO(b'Proposal Content'), 'proposal.zip')
    client.post(endpoint, data={'file': file})

    # Assert a post request is called with a url wmdev.saao.ac.za/wm/webservices/index.php
    assert run.requests.post.call_args[0][0] == 'wmdev.saao.ac.za/wm/webservices/index.php'

    # Assert a post request is called with the file type zip
    assert run.requests.post.call_args[1]['data'].content_type == 'application/zip'

    """
    End of test for the post request arguments
    """


def test_invalid_submit_proposal_message(client):
    """
    Test for the invalid multiple files attachment
    """
    endpoint = '/proposals'
    files = [(BytesIO(b'Proposal Content'), 'proposal.zip'), (BytesIO(b'Proposal Content'), 'proposal1.zip')]
    response = client.post(endpoint, data={'file': files})

    # Assert that an error message is returned for the multiple files attachment if more than one file attached
    assert response.data == b'Multiple files not allowed, please attach a single file.'
    """
    End of test for the invalid multi files attachment
    """

    """
    Test for the invalid file type
    """
    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.text')
    response = client.post(endpoint, data={'file': file})

    # Assert that an error message is returned for the invalid file type
    assert response.data == b'The file type of the attached file is no supported. Only zip file type supported'
    """
    End of test for the invalid file type
    """

    """
    Test for the user authentication
    """
    token = 'user-token-unauthenticated'
    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.zip')
    response = client.post(endpoint, data={'file': file}, headers={'Authentication': token})

    # Assert that an error message is returned for unauthenticated user token
    assert response.data == b'The user token is unauthentic, Please correct your credentials'
    """
    End of test for the user authentication
    """

    """
    Test for the user authorization
    """
    token = 'user-token-unauthorized'
    endpoint = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.zip')
    response = client.post(endpoint, data={'file': file}, headers={'Authentication': token})

    # Assert that an error message is returned for unauthenticated user token
    assert response.data == b'The user token is unauthorized, Please contact your administrator for permission'
    """
    End of test for the user authorization
    """
