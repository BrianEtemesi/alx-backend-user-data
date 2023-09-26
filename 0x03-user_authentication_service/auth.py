#!/usr/bin/env python3
"""
authentication module
"""
import bcrypt


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
