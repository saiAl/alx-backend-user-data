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

    def add_user(self, email, hashed_password) -> User:
        """Add a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
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
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError

        user = self._session.query(User).where(**kwargs).first()
        if user is None:
            raise NoResultFound

    def update_user(self, user_id, **kwargs) -> None:
        """Update a user's attribute in the database.
        """

        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.merge(user)
        self._session.commit()
