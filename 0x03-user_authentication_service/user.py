#!/usr/bin/env python3
"""
SQL Alchemy model User for table users
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    class representation of a User
    """

    # specify table name for this model
    __tablename__ = 'users'

    # define table columns
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
