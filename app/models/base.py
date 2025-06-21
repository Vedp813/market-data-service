"""
This module provides the declarative base class for SQLAlchemy ORM models.
All models should inherit from `Base` to ensure proper table and metadata registration.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()