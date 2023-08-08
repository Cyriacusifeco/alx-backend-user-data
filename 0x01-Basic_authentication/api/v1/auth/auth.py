#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class for API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        :param path: The path of the request.
        :type path: str
        :param excluded_paths: List of paths that are excluded from
        authentication.
        :type excluded_paths: List[str]
        :return: True if authentication is required, False otherwise.
        :rtype: bool
        """
        if path is None or not excluded_paths:
            return True
        
        # Add trailing slash to path for slash tolerance
        path_with_slash = path if path.endswith('/') else path + '/'
        
        for excluded_path in excluded_paths:
            # Add trailing slash to excluded_path for slash tolerance
            excluded_path_with_slash = (
                excluded_path if excluded_path.endswith('/') else excluded_path + '/'
            )
            
            if path_with_slash.startswith(excluded_path_with_slash):
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the authorization header from the request.

        :param request: The Flask request object.
        :type request: Request
        :return: The authorization header value.
        :rtype: str
        """
        if request:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user based on the request.

        :param request: The Flask request object.
        :type request: Request
        :return: The current user.
        :rtype: TypeVar('User')
        """
        return None
