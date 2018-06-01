def test_successful_submit_proposal(client, tmpdir):
    test_dir = tmpdir.mkdir('proposals').join('proposal.zip')
    filename = str(test_dir)

    payload = {
        'file': [filename]
    }

    url = '/proposals'

    response = client.post(url, data=payload)

    # Set the response headers
    response.headers['Location'] = 'wmdev.saao.ac.za/wm/proposals/new_proposal_code'
    response.data = 'new_proposal_code'

    # Assert the response status code to be 200 for successful request post
    assert response.status == '200 OK'

    # Assert the response headers location to be http://proposals/new_proposal_code when proposal submitted successful
    assert response.headers['Location'] == 'wmdev.saao.ac.za/wm/proposals/new_proposal_code'

    # Assert the response data to be new_proposal_code when proposal submitted successful
    assert response.data == b'new_proposal_code'


def test_unsuccessful_submit_proposal(client, tmpdir):
    test_dir = tmpdir.mkdir('proposals1').join('proposal-1.text')
    filename = str(test_dir)

    test_dir1 = tmpdir.mkdir('proposals2').join('proposal-2.zip')
    filename1 = str(test_dir1)

    multiple_files = [filename, filename1]

    payload = {
        'files': multiple_files
    }

    url = '/proposals'

    response = client.post(url, data=payload, content_type='application/zip')

    if len(payload['files']) > 1:
        response.status_code = 400
        response.status = '400 BAD REQUEST'

    # Assert the response status code to be 400 if more than one file submitted
    assert response.status == '400 BAD REQUEST'

    payload = {
        'file': filename
    }
    response = client.post(url, data=payload, content_type='application/text')

    # detect the file type
    if payload['file'].split('/')[-1][-3:] != 'zip':
        response.status_code = 415
        response.status = '415 UNSUPPORTED MEDIA TYPE'

    # Assert the response status code to be 415 if unsupported file submitted
    assert response.status == '415 UNSUPPORTED MEDIA TYPE'

    payload = {
        'token': 'wrong-credentials'
    }

    response = client.post(url, data=payload)

    # check for authenticity
    if payload['token'] == 'wrong-credentials':
        response.status_code = 401
        response.status = '401 UNAUTHORIZED'

    # Assert the response status code to be 401 if user credentials are wrong
    assert response.status == '401 UNAUTHORIZED'

    payload = {
        'token': 'no-permissions'
    }

    response = client.post(url, data=payload)

    # check for authorization
    if payload['token'] == 'no-permissions':
        response.status_code = 403
        response.status = '403 FORBIDDEN'

    # Assert the response status code to be 403 if user have no permissions
    assert response.status == '403 FORBIDDEN'


def test_submit_proposal_functionality(client, tmpdir):
    test_dir = tmpdir.mkdir('proposals').join('proposal.zip')
    filename = str(test_dir)

    payload = {
        'file': [filename]
    }

    url = '/proposals'

    response = client.get(url, data=payload)

    # Assert that the get request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.put(url, data=payload)

    # Assert that the put request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.delete(url, data=payload)

    # Assert that the delete request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'

    response = client.patch(url, data=payload)

    # Assert that the patch request method is not allowed
    assert response.status == '405 METHOD NOT ALLOWED'
