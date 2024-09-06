#!/usr/bin/env python3
"""This module defines the `BasicAuth` class,
    which is a subclass of the `Auth`
        class from the `api.v1.auth.auth` module.
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from models.user import User
from typing import TypeVar


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
                else authorization_header[6:]
                )

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes a Base64-encoded authorization header string.

            Args:
                base64_authorization_header:
                    The Base64-encoded authorization header string.

            Returns:
                The decoded authorization header string,
                    or None if the decoding fails.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64.b64decode(
                    base64_authorization_header).decode('utf-8')
        except binascii.Error:
            return None

        return base64.b64decode(
                base64_authorization_header).decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the username and password
            from a decoded Base64 authorization header.

            Args:
                decoded_base64_authorization_header:
                    The decoded Base64 authorization header string.

            Returns:
                A tuple containing the username and password,
                    or (None, None) if the extraction fails.
        """
        return (
                (None, None) if decoded_base64_authorization_header is None
                or not isinstance(decoded_base64_authorization_header, str)
                or ':' not in decoded_base64_authorization_header
                else (
                    decoded_base64_authorization_header.split(':')[0],
                    decoded_base64_authorization_header.split(':')[-1]
                    )
                )

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Retrieves a user object based on
            email and password credentials.

            Args:
                user_email: The user's email address.
                user_pwd: The user's password.

            Returns:
                A user object if the credentials are valid,
                    or None if the user is not found or
                    the password is incorrect.
        """

        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            instance_list = User.search({"email": user_email})
            user = instance_list[0]
            if user.is_valid_password(user_pwd):
                return user
        except KeyError:
            pass

        return None
