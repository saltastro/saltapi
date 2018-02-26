import os
import tempfile
import traceback
from functools import wraps

from flask import Flask, jsonify, request, g, make_response, Response, render_template, send_file
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth
from raven.contrib.flask import Sentry

from data.proposal import summary_file
from data.technical_review import update_liaison_astronomers, update_reviews
from schema.query import schema
from util.action import Action
from util.error import InvalidUsage
from util.proposal_summaries import zip_proposal_summaries
from util.user import basic_login, get_user_token, is_valid_token, create_token

app = Flask(__name__)
CORS(app)
sentry = None
if os.environ.get('SENTRY_DSN'):
    sentry = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
else:
    app.debug = True
token_auth = HTTPTokenAuth(scheme='Token')
basic_auth = HTTPBasicAuth()
multi_auth = MultiAuth(HTTPBasicAuth, HTTPTokenAuth)


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
app.add_url_rule('/graphql', view_func=token_auth.login_required(GraphQLView.as_view('graphql', schema=schema, graphiql=False)))


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


@app.route("/proposal-summary", methods=['POST'])
@token_auth.login_required
def proposal_summary():
    data = request.json
    proposal_code = data['proposalCode']

    # check permission
    if not g.user.may_perform(Action.VIEW_PROPOSAL, proposal_code='2018-1-SCI-005'):
        raise InvalidUsage(message='You are not allowed to view the pdf summary of proposal {proposal_code}'
                        .format(proposal_code=proposal_code),
                           status_code=403)

    return send_file(summary_file(proposal_code))


@app.route("/proposal-summaries", methods=['POST'])
@token_auth.login_required
def proposal_summaries():
    data = request.json
    proposal_codes = data['proposalCodes']

    # check permission
    for proposal_code in proposal_codes:
        if not g.user.may_perform(Action.VIEW_PROPOSAL, proposal_code='2018-1-SCI-005'):
            raise InvalidUsage(message='You are not allowed to view the pdf summary of proposal {proposal_code}'
                            .format(proposal_code=proposal_code),
                               status_code=403)

    with tempfile.NamedTemporaryFile('wb') as f:
        zip_proposal_summaries(proposal_codes, f)
        return send_file(f.name, mimetype='application/zip', attachment_filename='proposal_summaries.zip')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'errors': 'Not found'}), 404)


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


if __name__ == '__main__':
    app.run(port=5001)

