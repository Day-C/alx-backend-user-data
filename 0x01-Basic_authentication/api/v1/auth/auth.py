#!/usr/bin/env python3
"""manage the Api authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """manage authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return false.
        Args:
            path: path to search for in path_list
            excluded_paths: list of pathsnot suported
        Return:
            true or false based on results.
        """

        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) < 1:
            return True
        if path in excluded_paths:
            return False
        if (path + '/') in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """return none."""

        if request is not None:
            if request.headers['Authorization']:
                return request.headers['Authorization']
            else:
                return None
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """returns None."""

        return None
