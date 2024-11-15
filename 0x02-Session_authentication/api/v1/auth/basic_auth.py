#!/usr/bin/env python3
"""Basic Authentication class."""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar

class BasicAuth(Auth):
    """implements simple authentication process."""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Handle base64 encoding."""

        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        typ = authorization_header[0:6]
        if typ == "Basic ":
            # print(authorization_header[6:])
            return authorization_header[6:]
        else:
            return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """decode an already encoded string."""

        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            # print(base64.b64decode(base64_authorization_header))
            data = base64.b64decode(base64_authorization_header).decode('utf-8')
            return data
        except:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """return a tuple of user credentials."""

        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            # slipt the decoded credentials once with a ':' delimeter
            credentials = decoded_base64_authorization_header.split(':', 1)
            return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Fetch user based on his credentials."""

        # if there  is no email or if it is not a string
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_email) is not str:
            return None

        user = User.search({"email": user_email})

        if user:
            # print(user_data[0].__dict__)
            if user[0].is_valid_password(user_pwd):
                return user[0]
            else: return None
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """GET credentials of the current user."""

        authorization_header = self.authorization_header(request)
        # print(f"comming closer to {authorization_header)
        encoded = self.extract_base64_authorization_header(authorization_header)
        decoded = self.decode_base64_authorization_header(encoded)

        usr_detl = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(usr_detl[0], usr_detl[1])
        return user
