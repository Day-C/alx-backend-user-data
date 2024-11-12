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
            credentials = decoded_base64_authorization_header.split(':')
            return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Fetch user based on his credentials."""

        # if there  is no email or if it is not a string
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_email) is not str:
            return None

        user_data = User.search({"email": user_email})

        for i in range(len(user_data)):
           print(user_data[i])
        if user_data:
            user = User(user_data)
            
            if user.is_valid_password(user_pwd):
                return user
            else: return None
        else:
            return None
