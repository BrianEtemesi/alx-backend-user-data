#!/usr/bin/env python3
"""
implementation of a session class
"""
from api.v1.auth.auth import Auth
import uuid


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
