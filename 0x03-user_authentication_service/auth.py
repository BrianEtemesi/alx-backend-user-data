#!/usr/bin/env python3
"""
authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    hashes a password
    """

    # convert password to array of bytes
    _bytes = password.encode('utf-8')

    # generate salt
    salt = bcrypt.gensalt()

    # return hashed password
    return bcrypt.hashpw(_bytes, salt)


class Auth:
    """
    Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register user in database
        """

        # check if user with passed email exists
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

        return user
