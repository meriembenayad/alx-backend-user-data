#!/usr/bin/env python3
""" 10. Sessions in Database """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """
            Creates and stores new instance of UserSession
            Returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return user_session

    def user_id_for_session_id(self, session_id=None):
        """
            Returns the User ID by requesting UserSession
            in the database based on session_id
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})

        if len(user_session) == 0:
            return None

        if self.session_duration <= 0:
            return user_session[0].get('user_id')

        created_time = user_session[0].created_at
        if (created_time +
                timedelta(seconds=self.session_duration) < datetime.utcnow()):
            return None

        return user_session[0].get('user_id')

    def destroy_session(self, request=None):
        """
            Destroys the UserSession based on the Session ID
            from the request cookie
        """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False

        user_session = UserSession.search({'session_id': session_cookie})
        if len(user_session) <= 0:
            return False

        del self.user_id_by_session_id[session_cookie]
        user_session[0].remove()

        return True
