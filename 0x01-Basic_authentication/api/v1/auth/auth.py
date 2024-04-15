#!/usr/bin/env python3
""" 3. Auth Class """
from flask import request
from typing import List, TypeVar

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
