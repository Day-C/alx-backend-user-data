#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.basic_auth import BasicAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth = getenv('AUTH_TYPE')


if auth:
    if auth == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth

        auth = BasicAuth()
    elif auth == "session_auth":
        from api.v1.auth.session_auth import SessionAuth

        auth = SessionAuth()
    else:
        from api.v1.auth.auth import Auth

        auth = Auth()


@app.before_request
def do_first():
    """function to run before any request."""

    if auth:
        ex_paths = ['/api/v1/status/', '/api/v1/unauthorized/']
        ex_paths.append('/api/v1/forbidden/')
        ex_paths.append('/api/v1/auth_session/login/')
        # print(auth.require_auth(request.path, ex_paths))

        if auth.require_auth(request.path, ex_paths) is False:
            pass
        else:
            auth_header = auth.authorization_header(request)
            session_cookie = auth.session_cookie(request)

            if auth_header is None and session_cookie is None:
                abort(401)
            if auth.authorization_header(request) is None:
                abort(401)
            # check current users credentialas
            if auth.current_user(request) is None:
                abort(403)
            request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """

    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler."""

    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """Not allowed t access resource handler."""

    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
