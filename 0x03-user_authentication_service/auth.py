#!/usr/bin/env pyhton3
"""Module for password hashing.
"""
import bcrypt
from db import DB


def _hash_password(password):
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

    def register_user(self, email, password):
        pass
