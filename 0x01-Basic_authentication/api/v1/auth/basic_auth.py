#!/usr/bin/env python3
"""
implementation of a basic authentication class
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from models.user import User
from typing import TypeVar


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

        email, pwd = decoded_base64_authorization_header.split(":", 1)
        return email, pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns a Userr instance based on their email and password
        """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None

        # search for object with matching email
        try:
            results = User.search(attributes={"email": user_email})
        except Exception:
            return None

        if len(results) > 0:
            user_obj = results[0]

            # validate password of found user object
            if user_obj.is_valid_password(user_pwd):
                return user_obj
            else:
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64_str = self.extract_base64_authorization_header(auth_header)
        decoded_b64 = self.decode_base64_authorization_header(b64_str)
        credentials = self.extract_user_credentials(decoded_b64)
        email = credentials[0]
        pwd = credentials[1]
        user_obj = self.user_object_from_credentials(email, pwd)

        req_list = [auth_header, b64_str, decoded_b64, email, pwd, user_obj]

        if None in req_list:
            return None
        else:
            return user_obj
