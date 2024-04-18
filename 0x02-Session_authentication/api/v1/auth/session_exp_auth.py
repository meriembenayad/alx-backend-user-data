#!/usr/bin/env python3
""" 9. Expiration? """
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ A sessionAuth class with expiration to manage API authentication """

    def __init__(self):
        """ Initialize the session auth from SESSION_DURATION env variable """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID """
        if session_id is None:
            return None

        user_session = self.user_id_by_session_id.get(session_id)
        if user_session is None:
            return None

        if self.session_duration <= 0:
            return user_session.get('user_id')

        created_time = user_session.get('created_at')
        if created_time is None:
            return None

        if (created_time +
                timedelta(seconds=self.session_duration)) < datetime.now():
            return None

        return user_session.get('user_id')
