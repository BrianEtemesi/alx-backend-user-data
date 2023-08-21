#!/usr/bin/env python3
"""
session authentication routes
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenicate_session() -> None:
    """
    handles session authentication
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400

    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    # search for user using email attribute
    results = User.search(attributes={'email': email})

    if len(results) > 0:
        user = results[0]

        # validate password for the found user object
        if user.is_valid_password(pwd):

            from api.v1.app import auth

            # create session id from user id
            session_id = auth.create_session(user.id)

            # set cookie to the response
            response = jsonify(user.to_json())
            key = os.getenv('SESSION_NAME', 'my_session_id')
            response.set_cookie(key, session_id)

            return response
        else:
            return jsonify({"error": "wrong password"}), 401
    else:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout_session() -> None:
    """
    handles logout from session
    """
    from api.v1.app import auth

    # delete session id
    del_status = auth.destroy_session(request)

    if del_status:
        return jsonify({}), 200
    else:
        abort(404)
