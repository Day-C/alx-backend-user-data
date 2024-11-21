#!/usr/bin/env python3
""" creata an sqlalchemy module for Users tabe."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class User(Base):
    """users table structure."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    rest_token = Column(String(250), nullable=True)

