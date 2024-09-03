#!/usr/bin/env python3
"""This module defines the `BasicAuth` class,
    which is a subclass of the `Auth`
        class from the `api.v1.auth.auth` module.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic authentication implementation.
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64-encoded authorization header
            from a given string.

            Args:
                authorization_header: The authorization header string.

            Returns:
                The Base64-encoded portion of the authorization header,
                    or None if the header is invalid.

        """
        return (
                None if authorization_header is None
                or not isinstance(authorization_header, str)
                or authorization_header[:6] != 'Basic '
                else authorization_header[6:]`:s
                )
