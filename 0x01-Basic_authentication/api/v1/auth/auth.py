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
        return False

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
