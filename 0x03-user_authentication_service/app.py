#!/usr/bin/env python3
""" 6. Basic Flask app """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
