#!/usr/bin/env python3
"""
basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from api.v1.views.users import User


class BasicAuth(Auth):
    """ Basic Authentication class """
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """
        Extract the Base64 part of the Authorization header for
        Basic Authentication.

        :param authorization_header: The Authorization header value.
        :type authorization_header: str
        :return: The Base64 part of the Authorization header.
        :rtype: str
        """
        if authorization_header is None or not isinstance(
                authorization_header,
                str
                ):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """
        Decode a Base64 authorization header value to a UTF8 string.

        :param base64_authorization_header: The Base64 authorization
        header value.
        :type base64_authorization_header: str
        :return: The decoded value as UTF8 string.
        :rtype: str
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header,
                str
                ):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_bytes.decode('utf-8')
            return decoded_value
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Extract user email and password from the Base64 decoded value.

        :param decoded_base64_authorization_header: The decoded Base64
        authorization header value.
        :type decoded_base64_authorization_header: str
        :return: A tuple containing user email and user password.
        :rtype: tuple
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str
                ):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> User:
        """
        Get the User instance based on email and password.

        :param user_email: User's email.
        :type user_email: str
        :param user_pwd: User's password.
        :type user_pwd: str
        :return: User instance if found and password is valid, otherwise None
        :rtype: User
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> User:
        """
        Get the User instance for a request.

        :param request: Flask request object.
        :type request: flask.Request
        :return: User instance if authorized, otherwise None.
        :rtype: User
        """
        if request is None:
            return None

        authorization_header = request.headers.get("Authorization")
        if authorization_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                authorization_header
                )
        if base64_auth_header is None:
            return None

        decoded_base64 = self.decode_base64_authorization_header(
                base64_auth_header
                )
        if decoded_base64 is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_base64)
        if user_email is None or user_pwd is None:
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
