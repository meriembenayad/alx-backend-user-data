#!/usr/bin/env python3
""" 4. Hash password """
from user import User
from bcrypt import hashpw, gensalt


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
