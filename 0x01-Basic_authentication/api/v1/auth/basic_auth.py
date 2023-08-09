#!/usr/bin/env python3
"""
basic auth module
"""
from api.v1.auth.auth import Auth
import base64


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
