import json
import os
import tempfile
import traceback
import uuid
import base64
import magic
import zipfile
import requests
import xml.etree.ElementTree as ET

from functools import wraps
from zipfile import ZipFile
from flask import Flask, jsonify, request, g, make_response, Response, render_template, send_file, abort
from flask_graphql import GraphQLView
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth
from flask_socketio import SocketIO, emit
from raven.contrib.flask import Sentry

from data.completion_comment import update_completion_comments
from data.proposal import summary_file, latest_version, latest_semester
from data.blocks import get_blocks_status
from data.technical_review import update_liaison_astronomers, update_reviews
from data.user.user import update_tac_members, remove_tac_members
from schema.query import schema
from util.action import Action
from util.error import InvalidUsage
from util.proposal_summaries import zip_proposal_summaries
from util.user import basic_login, get_user_token, is_valid_token, create_token

app = Flask(__name__)
# configure socket to the application
socketio = SocketIO(app)
# Set CORS options on app configuration
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
sentry = None
if os.environ.get('SENTRY_DSN'):
    sentry = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
else:
    app.debug = True
token_auth = HTTPTokenAuth(scheme='Token')
basic_auth = HTTPBasicAuth()
multi_auth = MultiAuth(HTTPBasicAuth, HTTPTokenAuth)


def get_app():
    return app


@token_auth.verify_token
def verify_token(token):
    g.user_id = None
    try:
        is_valid = is_valid_token(token)

        return is_valid
    except:
        return False


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return basic_login(username, password)


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with Web Manager credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/proposals', methods=['POST'])
@token_auth.login_required
def submit_proposals():
    username = g.user.username
    password = os.environ.get('SDB_ACCESS_KEY')
    base_url = os.environ.get('WM_WEB_SERVICES')

    file = request.get_data()
    # Checks if the file is attached for submission
    # If it is not attached abort with the response status code 400
    if file == b'':
        abort(make_response(jsonify(error="No file is attached"), 400))

    tmp_dir = os.path.join(tempfile.gettempdir(), 'proposal_content')

    # Creating a temporary file with the content of the attached file
    with open(tmp_dir, 'wb+') as output:
        output.write(file)

    # Checks if the attached file type is a zip
    if zipfile.is_zipfile(tmp_dir):
        abort(make_response(jsonify(error="Only zip file is supported"), 415))

    # Setting a post request parameters
    files = {
        'proposal_content': open(tmp_dir, 'rb+')
    }

    data = {
        "method": 'sendProposal',
        "username": base64.b64encode(username.encode('utf-8')),
        "password": base64.b64encode(password.encode('utf-8')),
        "asyncCode": '',
        "proposalCode": 'Unsubmitted-001',
        "emails": False,
        "retainProposalStatus": False,
        "noValidation": False,
        "anySemester": False,
        "isAPI": True
    }

    # Making a post request
    response = requests.post(base_url, files=files, data=data)

    # Form a response to conform with the API specs
    if response.status_code == 200:
        make_rsp = make_response(
            json.dumps({'proposal_code': response.json()['Proposal_Code']}),
        )
        make_rsp.headers['Location'] = 'http://localhost:5001/proposals/' + response.json()['Proposal_Code']
        make_rsp.headers['Content-Type'] = 'application/json'
    else:
        make_rsp = make_response(
            json.dumps({'error': response.json()['Error']}),
            response.status_code
        )
        make_rsp.headers['Content-Type'] = 'application/json'

    # Returning a response
    return make_rsp


@app.route("/proposals/<string:proposal_code>", methods=['GET', 'PATCH'])
@token_auth.login_required
def get_or_update_proposal(proposal_code):
    if request.method == 'GET':
        # Checks if the {proposal_phase} query parameter does not exist
        if 'proposal_phase' not in request.args:
            phase = None
        else:
            phase = request.args['proposal_phase']

        return get_proposal(proposal_code, phase)

    elif request.method == 'PATCH':

        file = request.get_data()

        return update_proposal(proposal_code, file)


def get_proposal(proposal_code, phase):
    # Checks if the proposal phase is not equal to 1, 2 or None
    if phase not in ['1', '2', None]:
        abort(make_response(jsonify(error='Bad request, only values 1 and 2 allowed for proposal_phase'), 400))

    try:
        # Form a url pointing to the proposal's location
        url = '{}{}/{}/{}.zip'.format(
            os.environ.get('PROPOSALS_DIR'),
            proposal_code,
            latest_version(proposal_code, phase),
            proposal_code)

        # Include the retrieved file in a response with the status code 200
        make_rsp = make_response(send_file(url, as_attachment=True))
        make_rsp.status_code = 200
        make_rsp.headers['Content-Disposition'] = 'attachment; filename={}.zip'.format(proposal_code)

        # return the response
        return make_rsp
    except Exception as e:
        abort(make_response(jsonify(error=str(e)), 404))


def update_proposal(proposal_code, file):
    username = g.user.username
    password = os.environ.get('SDB_ACCESS_KEY')
    base_url = os.environ.get('WM_WEB_SERVICES')

    # Checks if the file is attached
    if file == b'':
        abort(make_response(jsonify(error="No file is attached"), 400))

    tmp_dir = os.path.join(tempfile.gettempdir(), proposal_code)

    # Creating a temporary file with the content of the attached file
    with open(tmp_dir, 'wb+') as output:
        output.write(file)

    # Checks if the attached file type is a zip
    if zipfile.is_zipfile(tmp_dir):
        abort(make_response(jsonify(error="Only zip file is supported"), 415))

    # Setting a put request parameters
    files = {
        'proposal_content': open(tmp_dir, 'rb+')
    }

    data = {
        "method": 'sendProposal',
        "username": base64.b64encode(username.encode('utf-8')),
        "password": base64.b64encode(password.encode('utf-8')),
        "asyncCode": '',
        "proposalCode": proposal_code,
        "emails": False,
        "retainProposalStatus": False,
        "noValidation": False,
        "anySemester": False,
        "isAPI": True
    }

    # Creating a post request
    response = requests.post(base_url, files=files, data=data)

    # Form a response to conform with the API specs
    if response.status_code == 200:
        make_rsp = make_response()
        make_rsp.status_code = 204
    else:
        make_rsp = make_response(
            json.dumps({'error': response.json()['Error']}),
            response.status_code
        )
        make_rsp.headers['Content-Type'] = 'application/json'

    # Returning a response
    return make_rsp


@app.route("/proposals/<string:proposal_code>/blocks/<string:block_code>", methods=['GET'])
@token_auth.login_required
def get_block(proposal_code, block_code):
    try:
        # Form a url pointing to the proposal's Include location
        xml = '{}{}/Included/Block-{}-{}.xml'.format(
            os.environ.get('PROPOSALS_DIR'),
            proposal_code,
            block_code,
            latest_semester(proposal_code)
        )

        zip_file = zip_block_content(xml)

        filename = '{}-{}'.format(proposal_code, block_code)
        # return the response with the file
        return send_file(
            zip_file,
            attachment_filename=filename,
            as_attachment=True, mimetype='application/zip'
        )
    except:
        abort(make_response(jsonify(error="Block not found."), 404))


def zip_block_content(xml, attachments_dir=None):

    # root directory for relative file paths
    if attachments_dir:
        root_dir = attachments_dir
    elif not hasattr(xml, 'read'):
        root_dir = os.path.abspath(os.path.join(xml, os.path.pardir))
    else:
        root_dir = None

    # parse the xml for referenced files
    attachments = {}

    # holds the block zip content
    zip_file = os.path.join(tempfile.gettempdir(), 'block_content')

    tree = ET.parse(xml)
    root = tree.getroot()

    for e in root.iter():
        tag = (e.tag.split('}')[-1])  # element name without namespace
        if tag == 'Path':

            attachment_path = e.text.strip().split('/')[-1]

            if attachment_path in ('automatic', 'auto-generated'):
                continue

            # get the absolute path
            if not os.path.isabs(attachment_path):
                if not root_dir:
                    raise Exception('The attachment path {path} is relative, but no attachment directory was supplied'
                                    .format(path=attachment_path))
                attachment_path = os.path.join(root_dir, attachment_path)

            if not os.path.isfile(attachment_path):
                raise Exception('{path} does not exist or is no file'.format(path=attachment_path))

            # save the real path and the path for the zip file, and update the XML
            extension = os.path.splitext(attachment_path)[1]
            path_in_zip = '{uuid}{extension}'.format(uuid=uuid.uuid4(), extension=extension)

            e.text = path_in_zip
            if attachment_path not in attachments:
                attachments[attachment_path] = path_in_zip

        # create the zip file
        with ZipFile(zip_file, 'w') as z:
            root_tag = root.tag.split('}')[-1]
            z.writestr('{name}.xml'.format(name=root_tag), ET.tostring(root, encoding='UTF-8'))
            for real_path, zip_path in attachments.items():
                z.write(real_path, zip_path)

    return zip_file


@app.route("/proposals/<string:proposal_code>/blocks/status/<string:blocks_status>", methods=['GET'])
@token_auth.login_required
def get_blocks(proposal_code, blocks_status):
    block_status_id = None

    # Checks for the requested status and assign the equivalent status ID for the easy database querying.
    if blocks_status == 'ACTIVE':
        block_status_id = 1
    elif blocks_status == 'ONHOLD':
        block_status_id = 2
    elif blocks_status == 'DELETED':
        block_status_id = 3
    elif blocks_status == 'SUPERSEDED':
        block_status_id = 4
    elif blocks_status == 'COMPLETED':
        block_status_id = 5
    elif blocks_status == 'NOTSET':
        block_status_id = 6
    elif blocks_status == 'EXPIRED':
        block_status_id = 7

    blocks_code = get_blocks_status(proposal_code, block_status_id)
    # Checks if the blocks with the specified status exist.
    if not blocks_code:
        abort(make_response(jsonify(error="Blocks not found."), 404))

    blocks = []
    # Formatting the data for easy use.
    for i in blocks_code:
        blocks.append({'block_code': blocks_code[i], 'status': blocks_status})
    # Creating a response
    response = make_response(json.dumps(blocks))
    response.headers['Content-Type'] = 'application/json'
    # Returning a response.
    return response


@app.route("/token", methods=['POST'])
def token():
    if request.json:
        tok = get_user_token(request.json)
        if "errors" in tok:
            raise InvalidUsage(message=tok, status_code=400)
        return jsonify({"user": {"token": tok}}), 200

    return jsonify({"errors": {"global": "Invalid user"}}), 401


@app.route("/token/<username>")
@token_auth.login_required
def other_user_token(username):
    # check permission
    if not g.user.may_perform(Action.SWITCH_USER):
        raise Exception('You are not allowed to switch users')

    try:
        tok = create_token(username)
        return jsonify({"user": {"token": tok}}), 200
    except Exception as e:
        return jsonify({"errors": {"global": str(e)}}), 200


def f():
    if True:
        return

    return


app.add_url_rule('/graphiql', view_func=requires_auth(GraphQLView.as_view('graphiql', schema=schema, graphiql=True)))
app.add_url_rule('/graphql',
                 view_func=token_auth.login_required(GraphQLView.as_view('graphql', schema=schema, graphiql=False)))


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/liaison-astronomers", methods=['POST'])
@token_auth.login_required
def liaison_astronomers():
    data = request.json
    assignments = data['assignments']
    update_liaison_astronomers(assignments)
    return jsonify(dict(success=True))


@app.route("/technical-reviews", methods=['POST'])
@token_auth.login_required
def technical_reviews():
    data = request.json
    semester = data['semester']
    reviews = data['reviews']
    update_reviews(semester=semester, reviews=reviews)
    return jsonify(dict(success=True))


@app.route("/completion-comments", methods=['POST'])
@token_auth.login_required
def completion_comment():
    data = request.json
    print(data)
    semester = data['semester']
    completion_comments = data['completionComments']
    update_completion_comments(semester=semester, completion_comments=completion_comments)
    return jsonify(dict(success=True))


@app.route("/update-tac-members", methods=['POST'])
@token_auth.login_required
def tac_members_update():
    """
    it update the tac members or add new tac members of a given partner.
    if member exist it will update else add
    Request
    ----------
        partner: str
            partner code like "RSA"
        members: iterable
            an array of object of shape {member: 'user-1', is_chair: 0}

    Returns
    -------
        success: bool
            Bool indicating whether the users had been updated/added or not.
    """
    data = request.json
    partner = data['partner']
    members = data['members']
    update_tac_members(partner=partner, members=members)
    return jsonify(dict(success=True))


@app.route("/remove-tac-members", methods=['POST'])
@token_auth.login_required
def tac_members_delete():
    """
    it remove the tac members which are given of a given partner.
    Request
    ----------
        partner: str
            partner code like "RSA"
        members: iterable
            an array of object of shape {member: 'user-1', is_chair: 0}

    Returns
    -------
        success: bool
            Bool indicating whether the users had been removed or not.
    """
    data = request.json
    partner = data['partner']
    members = data['members']
    remove_tac_members(partner=partner, members=members)
    return jsonify(dict(success=True))


@app.route("/proposal-summary", methods=['POST'])
@token_auth.login_required
def proposal_summary():
    data = request.json
    proposal_code = data['proposalCode']
    semester = data['semester']
    if 'partner' in data:
        partner = data['partner']
    else:
        partner = 'All'

    # TODO: check permission
    if not g.user.may_perform(Action.DOWNLOAD_SUMMARY, proposal_code=proposal_code, partner=partner):
        raise InvalidUsage(message='You are not allowed to view the pdf summary of proposal {proposal_code}'
                           .format(proposal_code=proposal_code),
                           status_code=403)

    return send_file(summary_file(proposal_code, semester))


@app.route("/proposal-summaries", methods=['POST'])
@token_auth.login_required
def proposal_summaries():
    data = request.json
    proposal_codes = data['proposalCodes']
    semester = data['semester']
    if 'partner' in data:
        partner = data['partner']
    else:
        partner = 'All'

    # check permission
    for proposal_code in proposal_codes:
        if not g.user.may_perform(Action.DOWNLOAD_SUMMARY, proposal_code=proposal_code, partner=partner):
            raise InvalidUsage(message='You are not allowed to view the pdf summary of proposal {proposal_code}'
                               .format(proposal_code=proposal_code),
                               status_code=403)

    with tempfile.NamedTemporaryFile('wb') as f:
        zip_proposal_summaries(proposal_codes, semester, f)
        return send_file(f.name, mimetype='application/zip', attachment_filename='proposal_summaries.zip')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'errors': 'Not found'}), 404)


@app.errorhandler(405)
def not_found(error):
    make_resp = make_response()
    make_resp.status_code = 405
    make_resp.headers['Content-Type'] = 'application/json'
    return make_resp


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'errors': 'Something is wrong'}), 500)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return make_response(jsonify(error.to_dict()), error.status_code)


@app.errorhandler(Exception)
def handle_exception(error):
    if sentry:
        sentry.captureException()
    else:
        traceback.print_exc()
        print('Set the SENTRY_DSN environment variable to log to Sentry instead of the command line.')
    return make_response(jsonify(dict(error='Sorry, there has been an internal server error. :-(')), 500)


@socketio.on('liaison socket')
def liaison_socket(data):
    emit('broadcast new liaison', data, broadcast=True)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    socketio.run(app, port=5001)
