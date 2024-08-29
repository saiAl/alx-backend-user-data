#!/usr/bin/env python3
from typing import ByteString
import bcrypt


def hash_password(password: str) -> ByteString:
    """ returns a salted, hashed password"""
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())
