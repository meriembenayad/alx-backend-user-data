#!/usr/bin/env python3
""" 6. Basic Flask app """
from flask import Flask, jsonify, request, abort, make_response, redirect
# 7. Register user
from auth import Auth

app = Flask(__name__)
# 7.
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ 6. method return JSON payload """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """ 7. method register a user """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': f'{email}', 'message': 'user created'}), 200
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ 11. Log in """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if login info correct
    user = AUTH.valid_login(email=email, password=password)
    if not user:
        abort(401)

    # Create & store a new session for the user
    session_id = AUTH.create_session(email=email)
    if session_id:
        # Create a response
        response = make_response(
            jsonify({'email': f'{email}', 'message': 'logged in'}), 200)
        # Set the session as a cookie
        response.set_cookie('session_id', session_id)

        return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ 14. Log out """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ 15. User Profile """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({'email': user.email}, 200)
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
