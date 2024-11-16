#!/usr/bin/env python3
"""Session authentication."""
from api.v1.auth.basic_auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """ Session authentication class structure."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user id."""

        if user_id is None or type(user_id) is not str:
            return None
        else:
            # create a session id and add to the session list
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrives a users id based on the session id."""

        if session_id is None or type(session_id) is not str:
            return None
        users_id = self.user_id_by_session_id.get(session_id, None)
        if users_id:
            return users_id

    def current_user(self, request=None) -> TypeVar('User'):
        """shows info on the current user."""

        sess_id = self.session_cookie(request)
        print(sess_id)
        usr_id = self.user_id_for_session_id(sess_id)
        print(usr_id)
        user = User.get(usr_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """DELETEs an existing session."""

        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False
        user_id = self.session_cookie(request)
        if user_id is None:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
