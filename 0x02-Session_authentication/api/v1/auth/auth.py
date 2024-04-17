#!/usr/bin/env python3
""" 3. Auth Class """
from flask import request
from typing import List, TypeVar
# 4. Session cookie
from os import getenv

User = TypeVar('User')


class Auth:
    """ Class Auth for managing API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require authentication """
        # if path is None
        if path is None:
            return True

        # if excluded_path is None or empty
        if not excluded_paths:
            return True

        # Ensuring the path ends with a slash
        syntax_path = path.rstrip('/') + '/'

        # Check if the path in excluded_paths
        for excluded_path in excluded_paths:
            # Check if the excluded path ends with (*)
            if excluded_path.endswith('*'):
                # remove (*) from excluded_path
                excluded_path_without_wildcard = excluded_path[:-1]
                # Check if path starts with excluded_path (excluding *)
                if syntax_path.startswith(excluded_path_without_wildcard):
                    return False
            else:
                # Check if the path is exactly the same as the excluded path
                if syntax_path == excluded_path:
                    return False

        # if the excluded_paths not match
        return True

    def authorization_header(self, request=None) -> str:
        """ Get the authorization header """
        # if request is None or doesn't contains the header key `Authorization`
        if request is None:
            return None
        # return the value of the header request `Authorization`
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user """
        return None

    def session_cookie(self, request=None):
        """
            4. Session cookie
            Returns a cookie value from a request
        """
        if request is None:
            return None

        return request.cookies.get(getenv('SESSION_NAME'))
