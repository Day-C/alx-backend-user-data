#!/usr/bin/env python3
from user imort User
from typing import TypeVar
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(email: str, password: str) -> TypeVar('User'):
        """register users"""

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User <user's email> already exists")
        pwd = self._hash_password(password)
        usr = self._db.add_user(email, pwd)
        return usr

