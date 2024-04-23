#!/usr/bin/env python3
""" 4. Hash password """
from user import User
from bcrypt import hashpw, gensalt, checkpw
# 5. Register user
from db import DB
from sqlalchemy.orm.exc import NoResultFound
# 9. Generate UUIDs
from uuid import uuid4


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
