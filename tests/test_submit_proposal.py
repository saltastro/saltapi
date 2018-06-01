

def test_successful_submit_proposal(client, tmpdir):
    test_dir = tmpdir.mkdir('proposals').join('proposal.zip')
    filename = str(test_dir)

    data = {
        'file': filename
    }

    url = '/proposals'

    response = client.post(
        url,
        data=data
    )

    # Assert the response status code to be 200 for successful request post
    assert response.status_code == 200

    # Assert the response
