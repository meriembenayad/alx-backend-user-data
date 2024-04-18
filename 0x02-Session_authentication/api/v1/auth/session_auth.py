#!/usr/bin/env python3
""" 1. Empty session """
from api.v1.auth.auth import Auth
from uuid import uuid4
# 6. Use Session ID for identifying a User
from models.user import User


class SessionAuth(Auth):
    """ 1. Empty session """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            2. creates a Session ID for a user_id
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            3. User ID for Session ID
            returns a User ID based on a Session ID
        """
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
            6. Use Session ID for identifying a User
            Returns a User instance based on a cookie value
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
            8. Logout
            Deletes the user session / logout
        """
        if request is None:
            return False

        Session_cookie = self.session_cookie(request)
        if not Session_cookie:
            return False

        user_id = self.user_id_for_session_id(Session_cookie)
        if not user_id:
            return False

        del self.user_id_by_session_id[Session_cookie]
        return True
