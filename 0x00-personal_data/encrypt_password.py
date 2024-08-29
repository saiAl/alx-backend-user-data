#!/usr/bin/env python3
""" Encrypting passwords """
from typing import ByteString
import bcrypt


def hash_password(password: str) -> ByteString:
    """ returns a salted, hashed password"""
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: ByteString, password: str):
    """ check of a given password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
