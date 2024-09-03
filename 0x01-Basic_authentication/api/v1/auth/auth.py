#!/usr/bin/env python3
"""This module provides an abstract base class
    for authentication in Flask applications.

    The Auth class defines the following methods:
        require_auth: Determines whether authentication
            is required for a given path.
        authorization_header: Extracts the authorization
            header from a request.
        current_user: Returns the current user based on the
            authorization header.

    Subclasses of Auth can implement these methods
        to provide specific authentication mechanisms.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Abstract base class for authentication in Flask applications.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines whether authentication is
            required for a given path.

            Args:
                path: The path to check.
                excluded_paths: A list of paths that do not
                    require authentication.

            Returns:
                True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Extracts the authorization header from a request.

            Args:
                request: The Flask request object.

            Returns:
                The authorization header value, or None if it is not present.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user based on
            the authorization header.

            Args:
                request: The Flask request object.

            Returns:
                The current user, or None if the user is not authenticated.
        """
        return None
