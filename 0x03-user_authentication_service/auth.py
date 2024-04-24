#!/usr/bin/env python3
""" 4. Hash password """
from user import User
from bcrypt import hashpw, gensalt, checkpw
# 5. Register user
from db import DB
from sqlalchemy.orm.exc import NoResultFound
# 9. Generate UUIDs
from uuid import uuid4
# 12. Find user by session ID
from typing import Union, TypeVar


def _hash_password(password: str) -> bytes:
    """
    4. Hash password
    Convert password to bytes (Hash it)
    """
    # Generate a random salt
    salt = gensalt()

    # Use salt to hash password
    hashed_password = hashpw(password.encode(), salt)

    return hashed_password


def _generate_uuid() -> str:
    """ 9. Generate uuid """
    id = str(uuid4())
    return id


# 5. Register user


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        5. Register user
        """
        # Check if user already exists
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        hashed_password = _hash_password(password=password)
        # decode hashed_password
        decoded_password = hashed_password.decode('utf-8')
        # Add new user to database
        user = self._db.add_user(email, decoded_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ 8. Credentials validation """
        try:
            user = self._db.find_user_by(email=email)
            # encode password & hashed_password in database
            hash_password = user.hashed_password.encode('utf-8')
            pwd = password.encode('utf-8')
            # check password
            checked_password = checkpw(pwd, hash_password)
            return checked_password
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ 10. Get session ID """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return 'None'

    def get_user_from_session_id(self,
                                 session_id: str
                                 ) -> Union[TypeVar('User'), None]:
        """ 12. Find user by session ID """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ 13. Destroy session """
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except NoResultFound:
            return None
