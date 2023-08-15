#!/usr/bin/env python3
"""
implementation of a basic authentication class
"""
from api.v1.auth.auth import Auth
import base64
import binascii


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        decodes the value of a base64 string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> str:
        """
        extracts credentials from encoded base64 string
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(":")
        return credentials[0], credentials[1]
