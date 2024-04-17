#!/usr/bin/env python3
""" 7. New view for Session Authentication """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        POST /auth_session/login
        Returns:
            - User object represented as JSON
            - Sets a cookie for the user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user_id)
    cookie_name = getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(cookie_name, session_id)
    return response
