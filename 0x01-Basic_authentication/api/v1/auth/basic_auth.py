#!/usr/bin/env python3
""" 6. Basic Auth """
from api.v1.auth.auth import Auth
# 8. Base64 decode
import base64


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
