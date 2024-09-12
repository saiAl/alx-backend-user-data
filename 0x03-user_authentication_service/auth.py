#!/usr/bin/env python3
"""Module for password hashing.
"""
import bcrypt
from db import DB
from user import User
import sqlalchemy


def _hash_password(password) -> bytes:
    """Hash a password using bcrypt.
    """
    return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
            )


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password) -> User:
        """Register a new user with the given email and password.
        """
        hash_password = _hash_password(password)
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except sqlalchemy.orm.exc.NoResultFound:
            pass
        user = self._db.add_user(email=email, hashed_password=hash_password)
        return user
