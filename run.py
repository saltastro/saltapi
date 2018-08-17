import json
import os
import tempfile
import traceback
import zipfile
from functools import wraps
import base64
from io import StringIO, BytesIO

import magic

import requests
from flask import Flask, jsonify, request, g, make_response, Response, render_template, send_file, abort, \
    send_from_directory
from flask_graphql import GraphQLView
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth
from flask_socketio import SocketIO
from raven.contrib.flask import Sentry

from data.proposal import summary_file, latest_version
from data.technical_review import update_liaison_astronomers, update_reviews
from data.user import update_tac_members, remove_tac_members
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
    username = os.environ.get('USERNAME')
    password = os.environ.get('SDB_ACCESS_KEY')
    base_url = os.environ.get('WM_WEB_SERVICES')

    file = request.get_data()
    # Checks if the file is attached for submission
    # If it is not attached abort with the response status code 400
    if file == b'':
        abort(make_response(jsonify(error="No file is attached"), 400))

    filename = 'proposal_content'
    # Creating a temporary file with the content of the attached file
    with open(os.path.join(tempfile.gettempdir(), filename), 'wb+') as output:
        output.write(file)
        output.close()
    # Make the file to be readable
    tmp_file = open(os.path.join(tempfile.gettempdir(), filename), 'rb+')
    # Retrieving the file type of the temporary created file
    file_type = magic.from_file(os.path.join(tempfile.gettempdir(), filename), mime=True)
    # Checks if the attached file type is a zip
    # If it is not a zip file abort with the response status code 415
    if file_type not in ['application/octet-stream', 'application/zip']:
        abort(make_response(jsonify(error="Only zip file is supported"), 415))
    # Setting a post request parameters
    files = {
        'proposal_content': tmp_file
    }

    data = {
        "method": 'SendProposal',
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
    # Creating a post request
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


@app.route("/proposals/<string:proposal_code>", methods=['GET'])
@token_auth.login_required
def get_proposal(proposal_code):

    proposal_phase = request.args['proposal_phase']
    # Forming a url that points to the proposals directory
    url = '{}/{}/{}/{}'.format(
        os.environ.get('PROPOSALS_DIR'),
        proposal_code,
        str(latest_version(proposal_code, proposal_phase)),
        proposal_code + ".zip"
    )

    # Creating a get request to retrieve a proposal
    response = requests.get(url)

    # Make a response to conform with the API specs
    if response.status_code == 200:
        make_rsp = make_response(response.content)
        make_rsp.headers['Content-Type'] = 'application/zip'

    else:
        make_rsp = make_response(
            json.dumps(response.json()),
            response.status_code
        )
        make_rsp.headers['Content-Type'] = 'application/json'

    # Returning the response
    return make_rsp


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
    partner = data['partner']

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
    partner = data['partner']

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


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    socketio.run(app, port=5001)
