import os
from flask import Flask, jsonify, request, g, make_response, Response, render_template
from flask_graphql import GraphQLView
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth
from functools import wraps
from flask_cors import CORS

from schema.query import schema
from schema.user import User

app = Flask(__name__)
app.debug = True
CORS(app)

token_auth = HTTPTokenAuth(scheme='Token')
basic_auth = HTTPBasicAuth()
multi_auth = MultiAuth(HTTPBasicAuth, HTTPTokenAuth)


@token_auth.verify_token
def verify_token(token):
    g.user_id = None
    try:
        is_valid = User.is_valid_token(token)

        return is_valid
    except:
        return False


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return User.basic_login(username, password)


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
        tok = User.get_user_token(request.json)
        if "errors" in tok:
            return jsonify(tok), 401
        return jsonify({"user": {"token": tok}}), 200

    return jsonify({"errors": {"global": "Invalid user"}}), 401


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


@app.route("/update-time-allocs", methods=['POST'])
@token_auth.login_required
def update_time_allocs():
    from util.time_allocations import update_time_allocations

    allocations = request.json['time_allocations']
    partner = request.json['partner']
    semester = request.json['semester']

    return jsonify({
        'result': update_time_allocations(allocations, partner, semester)
    })


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'errors': 'Not found'}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'errors': 'Fail to connect to sdb'}), 500)


if __name__ == '__main__':
    app.run(port=5001)

