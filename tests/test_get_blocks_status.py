import json
import pytest
from unittest.mock import patch


@pytest.mark.parametrize(('proposal_code', 'blocks_status',), (
    ('2018-1-SCI-030', 'ACTIVE',),
    ('2018-1-SCI-030', 'ONHOLD',),
    ('2018-1-SCI-030', 'COMPLETED',),
))
def test_get_blocks_status_successful(client, proposal_code, blocks_status, auth_header):
    with patch('run.get_blocks_status') as get_blocks_status:
        block_code = None
        if blocks_status == 'ACTIVE':
            block_code = 'BR9IJQYW'
            get_blocks_status.return_value = {0: block_code}
        elif blocks_status == 'ONHOLD':
            block_code = 'HEY5U7H3'
            get_blocks_status.return_value = {0: block_code}
        elif blocks_status == 'COMPLETED':
            block_code = 'A3DTW2L4'
            get_blocks_status.return_value = {0: block_code}

        proposal_code = '2018-1-SCI-030'
        blocks_status = 'COMPLETED'

        endpoint = '/proposals/{}/blocks/status/{}'.format(proposal_code, blocks_status)

        response = client.get(endpoint, headers=auth_header)

        # assert the status code when the file is retrieved successfully
        assert response.status_code == 200
        # assert the block code is returned with is correct status
        assert json.loads(response.data) == [{'block_code': block_code, 'status': blocks_status}]
        # assert the content type of the retrieved blocks status
        assert response.headers['Content-Type'] == 'application/json'


@pytest.mark.parametrize(('proposal_code', 'blocks_status',), (
    ('NOPROPOSAL', 'NOBLOCKS_STATUS',),
    ('2018-2-SCI-040', 'NOBLOCKS_STATUS',),
))
def test_get_blocks_status_not_found(client, proposal_code, blocks_status, auth_header):

    endpoint = '/proposals/{}/blocks/status/{}'.format(proposal_code, blocks_status)

    response = client.get(endpoint, headers=auth_header)

    # assert the status code when the proposal not found
    assert response.status_code == 404
    # assert the error message to contain 'proposal_code does not'
    assert 'not' in json.loads(response.data)['error']
    # assert the content type of the returned response
    assert response.headers['Content-Type'] == 'application/json'


def test_get_blocks_status_unauthorized(client):
    response = client.get('/proposals/proposal_code/blocks/status/any_status')

    # assert the status code for an unauthorized user
    assert response.status_code == 401


def test_get_proposal_disallowed_request_methods(client, auth_header):
    endpoint = '/proposals/proposal_code/blocks/status/any_status'
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
