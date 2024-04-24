#!/usr/bin/env python
""" 20. End-to-end integration test """
import requests


URL_BASE = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """ Register a new user """
    response = requests.post(f'{URL_BASE}/users',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'User Created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Try log in with wrong password """
    response = requests.post(f'{URL_BASE}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Log in with correct password """
    response = requests.post(f'{URL_BASE}/sessions',
                             data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'logged in'}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Try to access the profile without logging in """
    response = requests.get(f'{URL_BASE}/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Access the profile after logging in """
    response = requests.get(f'{URL_BASE}/profile',
                            cookies={'session_id': session_id})
    assert response.status_code == 200
    assert response.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """ Log out """
    response = requests.delete(f'{URL_BASE}/sessions',
                               cookies={'session_id': session_id})
    assert response.status_code == 302


def reset_password_token(email: str) -> str:
    """ Get a reset password token """
    response = requests.post(
        f'{URL_BASE}/reset_password', data={'email': email})
    assert response.status_code == 200
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update the password """
    response = requests.put(f'{URL_BASE}/reset_password', data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password})
    assert response.status_code == 200
    assert response.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
