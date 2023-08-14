#!/usr/bin/env python3
"""
implementation of a class to manage authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        to document later
        """
        if excluded_paths is None or excluded_paths == [] or path is None:
            return True

        # check path for slash
        if path and path[-1] != "/":
            path = path + "/"

        # check list for slashes
        for i in range(len(excluded_paths)):
            if excluded_paths[i] and excluded_paths[i][-1] != "/":
                excluded_paths[i] = excluded_paths[i] + "/"

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        to document later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        to document later
        """
        return None
