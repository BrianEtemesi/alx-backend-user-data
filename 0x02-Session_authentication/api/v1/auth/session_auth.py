#!/usr/bin/env python3
"""
implementation of a session class
"""
from api.v1.auth.auth import Auth
import uuid
from flask import request


class SessionAuth(Auth):
    """
    class representation of session auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session id for a user id
        """
        if user_id is None or type(user_id) != str:
            return None

        # create a session id
        session_id = str(uuid.uuid4())

        # set user id to session id in cls dictionary
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a user id based on a session id
        """
        if session_id is None or type(session_id) != str:
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)
