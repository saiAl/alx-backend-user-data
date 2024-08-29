#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt
import typing


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password"""
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check of a given password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
