#!/usr/bin/env python3
""" 6. Basic Auth """
from api.v1.auth.auth import Auth
# 8. Base64 decode
import base64
# 10. Basic - User object
from models.user import User
from typing import TypeVar

t_user = TypeVar('User')


class BasicAuth(Auth):
    """ BasicAuth class for """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
            7. Return Base64 part of the Authorization header
            for a Basic Authorization
        """
        if authorization_header is None:
            return None

        if not type(authorization_header) == str:
            return None

        if not authorization_header.startswith('Basic '):
            return None

        # Return the part of authorization_header after `Basic `
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
            8. Return decoded value of a Base64 string
            base64_authorization_header
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string
            decode_bytes = base64.b64decode(base64_authorization_header)
            # Convert the bytes to utf-8 string
            return decode_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
            9. Return the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string at `:`
        decoded_auth_header = decoded_base64_authorization_header
        user_email, user_password = decoded_auth_header.split(':')

        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
            10. Returns the User instance based on his email & password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for a user with the email
        users = User.search({'email': user_email})

        # if no user found or the password not valid
        if not users or not users[0].is_valid_password(user_pwd):
            return None

        # if user found
        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
            11. Overloads Auth & retrieve User instance for a request
        """
        # Get authorization_header
        auth_header = self.authorization_header(request)

        # Extract the Base64 part of the auth_header
        base64_auth_header = self.extract_base64_authorization_header(
                auth_header)

        # decode the Base64 part of auth_header
        decode_auth_header = self.decode_base64_authorization_header(
                base64_auth_header)

        # Extract user credentials from decoded Base64 part of auth_header
        user_email, user_pwd = self.extract_user_credentials(
                decode_auth_header)

        # Retreive the User instance based on the user credentials
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
