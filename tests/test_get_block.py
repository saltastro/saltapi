import json


def test_get_block_successful(client, auth_header):

    proposal_code = '2017-1-SCI-030'
    block_code = '8B8QPQ2S'

    endpoint = '/proposals/{}/blocks/{}'.format(proposal_code, block_code)

    response = client.get(endpoint, headers=auth_header)

    # assert the status code when the file is retrieved successfully
    assert response.status_code == 200
    # assert the content type of the retrieved file
    assert response.headers['Content-Type'] == 'application/zip'
    # assert the disposition to have file name with proposal code
    assert proposal_code in response.headers['Content-Disposition']


def test_get_block_not_found(client, auth_header):

    endpoint = '/proposals/2018-2-SCI-040/blocks/BLOCK'

    response = client.get(endpoint, headers=auth_header)

    # assert the status code when the proposal not found
    assert response.status_code == 404
    # assert the error message to contain 'proposal_code does not'
    assert 'not' in json.loads(response.data)['error']
    # assert the content type of the returned response
    assert response.headers['Content-Type'] == 'application/json'


def test_get_block_unauthorized(client):
    response = client.get('/proposals/proposal_code/blocks/block_code')

    # assert the status code for an unauthorized user
    assert response.status_code == 401


def test_get_proposal_disallowed_request_methods(client, auth_header):
    endpoint = '/proposals/proposal_code/blocks/block_code'
    # Assert the response status code for not allowed request method
    assert client.patch(endpoint, headers=auth_header).status_code == 405
    assert client.put(endpoint, headers=auth_header).status_code == 405
    assert client.post(endpoint, headers=auth_header).status_code == 405
    assert client.delete(endpoint, headers=auth_header).status_code == 405

    # Assert the response content type
    assert client.patch(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
    assert client.put(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
    assert client.post(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
    assert client.delete(endpoint, headers=auth_header).headers['Content-Type'] == 'application/json'
