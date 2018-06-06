from io import BytesIO
import json
from unittest.mock import MagicMock


def test_successful_submit_proposal(monkeypatch, client):
    # Creating the mocking substitute function for the post request/response to submitting proposal
    def mock_submit_proposal_post_request_response(*args, **kwargs):
        # setting up the response content
        return {
            'status': '200 OK',
            'status_code': 200,
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

    url = '/proposals'
    file = (BytesIO(b'Proposal Content'), 'proposal.zip')

    payload = {
        'file': file
    }

    response = client.post(url, data=payload)

    resp = json.loads(response.data)

    # Assert the response status code to be 200 for successful request post
    assert resp['status'] == '200 OK'

    # Assert the response content type to be a json when proposal submitted successful
    assert resp['headers']['Content-Type'] == "application/json"

    # Assert the response headers location to be http://proposals/new_proposal_code when proposal submitted successful
    assert resp['headers']['Location'] == 'wmdev.saao.ac.za/wm/proposals/new_proposal_code'

    # Assert the response data to be new_proposal_code when proposal submitted successful
    assert resp['body']['proposal-code'] == 'new_proposal_code'


def test_submit_proposal_disallowed_request_method(client):
    url = '/proposals'

    response = client.get(url)

    # Assert that the get request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url)

    # Assert that the put request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.delete(url)

    # Assert that the delete request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.patch(url)

    # Assert that the patch request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'


def test_submit_proposal_functionality(self, client):
    import run

    self.file_content = None

    # Creating the mocking substitute function for the post request/response to submitting proposal to get file content
    def get_file_content(*args, **kwargs):
        self.file_content = kwargs['data'].read()
        return self.file_content

    run.requests.post = get_file_content

    file = (BytesIO(b'Proposal Content'), 'proposal.zip')
    client.post('/proposals', data={'file': file})

    # Assert the proposal file content to be b'Proposal Content'
    assert self.file_content == b'Proposal Content'

    # Mocking the post request method using the MagicMock class for the post request/response to submitting proposal
    run.requests.post = MagicMock()

    file = (BytesIO(b'Proposal Content'), 'proposal.zip')
    client.post('/proposals', data={'file': file})

    # Assert a post request method is called once
    run.requests.post.assert_called_once()

    # Assert a post request is called with a url http://google.com/
    assert run.requests.post.call_args[0][0] == 'https://google.com/'

    # Assert a post request is called with the filename proposal.zip
    assert run.requests.post.call_args[1]['data'].filename == 'proposal.zip'

    # Assert a post request is called with the file type zip
    assert run.requests.post.call_args[1]['data'].content_type == 'application/zip'
