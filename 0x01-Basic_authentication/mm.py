#!/usr/bin/env python3
"""test the user model and its functionality."""
from models.user import User
from models.base import Base
user = User.search({"name": "Bob"})
print(user)
