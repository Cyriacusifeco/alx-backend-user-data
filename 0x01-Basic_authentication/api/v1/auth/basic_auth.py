#!/usr/bin/env python3
"""
basic auth module
"""
from api.v1.auth.auth import Auth


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
