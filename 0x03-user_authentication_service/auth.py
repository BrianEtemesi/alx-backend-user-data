#!/usr/bin/env python3
"""
authentication module
"""
import bcrypt
import uuid
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


def _generate_uuid() -> str:
    """
    returns a string representation of a new uuid
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        validates user credentials
        """
        # try locating user by email
        try:
            user = self._db.find_user_by(email=email)
            if user:
                # encode entered password
                encoded_pw = password.encode('utf-8')
                # compare entered pwd with user pwd
                return bcrypt.checkpw(encoded_pw, user.hashed_password)
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        creates sessions for users
        """
        # find user with corresponding email
        try:
            user = self._db.find_user_by(email=email)

            # if user is found, generate session id
            session_id = _generate_uuid()

            # update user with session id
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        gets user by their session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a user's session
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generates a reset password token for user
        """
        # get user by email
        user = self._db.find_user_by(email=email)

        # if user is found, generate token
        if user:
            token = _generate_uuid()

            # update user's reset token
            self._db.update_user(user.id, reset_token=token)

            return token
        else:
            raise ValueError
