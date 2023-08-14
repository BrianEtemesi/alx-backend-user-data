#!/usr/bin/env python3
"""
implementation of a basic authentication class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    basic authentiction class that inherits from Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        decodes base64 string from the auth header
        """
        if authorization_header is None or type(authorization_header) != str:
            return None

        if authorization_header.startswith("Basic "):
            return authorization_header[len("Basic "):]
        else:
            return None
