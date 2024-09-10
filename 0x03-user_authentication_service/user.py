#!/usr/bin/env python3
"""This module defines the User model for a database.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """Represents a user in the database.

        Attributes:
            id (int): The primary key of the user.
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.
            session_id (str): The user's current session ID.
            reset_token (str): The user's password reset token.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

