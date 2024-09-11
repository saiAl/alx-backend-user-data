#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """Add a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """Finds a user in the database by a given attribute.

            Args:
                **kwargs: Arbitrary keyword arguments,
                    where the key is an attribute of the User model

            Returns:
                User: The first user that matches the given criteria.

            Raises:
                InvalidRequestError:
                    If the required 'email' attribute
                        is not provided in kwargs.
                NoResultFound:
                    If no user is found with
                        the specified attribute.
        """
        key, value = tuple(kwargs.items())[0]

        users = self._session.query(User).all()
        for user in users:
            try:
                u = user if user.__getattribute__(key) == value else None
                if u is None:
                    raise NoResultFound
                else:
                    return user
            except AttributeError:
                raise InvalidRequestError

    def update_user(self, user_id, **kwargs):
        """ """
        pass
