#!/usr/bin/env python
"""
A simple app to create a JWT token.
"""
import os
import logging
import datetime
import functools
import jwt
from flask import Flask, jsonify, request, abort


JWT_SECRET = os.environ.get('JWT_SECRET', 'abc123abc1234')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


def _logger():
    '''
    Setup logger format, level, and handler.

    RETURNS: log object
    '''
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log


log = _logger()
log.debug("Starting with log level: %s" % LOG_LEVEL)
app = Flask(__name__)


def require_jwt(function):
    """
    Decorator to check valid jwt is present.
    """
    @functools.wraps(function)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except BaseException:  # pylint: disable=bare-except
            abort(401)
        return function(*args, **kws)
    return decorated_function


@app.route('/', methods=['POST', 'GET'])
def health():
    return jsonify("Healthy")


@app.route('/auth', methods=['POST'])
def auth():
    """
    Create JWT token based on email.
    """
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    if not email:
        log.error("No email provided")
        return jsonify({"message": "Missing parameter: email"}, 400)
    if not password:
        log.error("No password provided")
        return jsonify({"message": "Missing parameter: password"}, 400)
    body = {'email': email, 'password': password}
    user_data = body
    return jsonify(token=_get_jwt(user_data))


@app.route('/contents', methods=['GET'])
def decode_jwt():
    """
    Check user token and return non-secret data
    """
    if not 'Authorization' in request.headers:
        abort(401)
    data = request.headers['Authorization']
    token = str.replace(str(data), 'Bearer ', '')
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except BaseException:  # pylint: disable=bare-except
        abort(401)
    response = {'email': data['email'], 'exp': data['exp'], 'nbf': data['nbf']}
    return jsonify(**response)


def _get_jwt(user_data):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    payload = {
        'exp': exp_time,
        'nbf': datetime.datetime.utcnow(),
        'email': user_data['email']}
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
