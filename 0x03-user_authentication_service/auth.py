#!/usr/bin/env python3
"""Module for password hashing.
"""
import bcrypt
import sqlalchemy
from db import DB
from user import User
import uuid


def _hash_password(password) -> bytes:
    """Hash a password using bcrypt.
    """
    return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
            )


def _generate_uuid():
    """Generate uuid
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email, password) -> bool:
        """Check the password
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email):
        """Create a new session for a user identified by their email.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            pass
        return None

    def get_user_from_session_id(self, session_id):
        """Retrieve a user by their session ID.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            pass
        return None
