from io import BytesIO
import zipfile


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
