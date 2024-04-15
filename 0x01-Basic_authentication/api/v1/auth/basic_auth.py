#!/usr/bin/env python3
""" 6. Basic Auth """
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ BasicAuth class for """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
            Return Base64 part of the Authorization header
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
