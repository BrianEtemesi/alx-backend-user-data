#!/usr/bin/env python3
"""
flask application
"""

from flask import (Flask, jsonify, request, make_response,
                   abort, redirect, url_for)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def payload():
    """
    returns  json payload
    """
    response_data = {"message": "Bienvenue"}
    return jsonify(response_data)


@app.route('/users', methods=['POST'])
def users():
    """
    registers a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        response_data = {"email": "{}".format(email),
                         "message": "user created"}
        return jsonify(response_data)
    except ValueError:
        response_data = {"message": "email already registered"}
        return jsonify(response_data), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    log in user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # validate user credentials and create session
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response_data = {"email": "{}".format(email),
                         "message": "logged in"}
        response = make_response(jsonify(response_data))
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    logs out user by destroying user session
    """
    # retrieve session id from request cookie
    session_id = request.cookies.get('session_id')

    # find user with retrieved session id
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('payload'))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
