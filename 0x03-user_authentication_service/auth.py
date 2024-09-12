#!/usr/bin/env pyhton3
"""Module for password hashing.
"""
import bcrypt


def _hash_password(passwd):
    """Hash a password using bcrypt.
    """
    return bcrypt.hashpw(
            passwd.encode('utf-8'), 
            bcrypt.gensalt()
            )
