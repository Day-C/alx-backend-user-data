#!/usr/bin/emv python3
""" Module for authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
# from api.v1.app import auth


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def user_login():
    """ POST /api/v1/auth_session/login"""

    # get email and password from from
    mail = request.form.get("email", None)
    pwd = request.form.get("password", None)

    # check for valid  email and passwor
    if mail is None:
        return jsonify({"error": "email missing"}), 400
    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user instance then check password
    usr_list = User.search({"email": mail})
    user = usr_list[0]
    if user:
        # create a session id for user id
        from api.v1.app import auth

        if user.is_valid_password(pwd) is False:
            return jsonify({"error": "wrong password"}), 401
        usr = auth.create_session(user.id)
        return jsonify(user.to_json())
    else:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=["DELETE"])
def delete_session():
    """Delete a session."""
    from api.v1.app import auth

    if auth.destroy_session(request) is False:
        abort(404)
