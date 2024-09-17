"""
BaseModel for Flask-SQLAlchemy

This module defines the `BaseModel` class, which serves as an abstract base class for other models
in the application. It includes common fields for tracking the creation and last modification times
of records.

Dependencies:
- `db`: SQLAlchemy database instance from `poultry_manager`.
- `NetworkTime`: A utility class from `poultry_manager.live_time` to fetch network time.

Usage:
To use this base model, other model classes should inherit from `BaseModel`.

"""

from poultry_manager import db
from poultry_manager.live_time import NetworkTime

# Fetch the current network time for default timestamps
ntplib_time = NetworkTime.network_time()


class BaseModel(db.Model):
    """
    Abstract base model class for including `created_at` and `updated_at` fields.

    Attributes:
        id (int): Primary key of the model, automatically generated integer.
        created_at (datetime): Timestamp when the record was created, default is the current network time.
        updated_at (datetime): Timestamp when the record was last updated, default is the current network time,
                              automatically updated on record modification.
    """
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    updated_at = db.Column(db.DateTime(), nullable=False, default=ntplib_time, onupdate=ntplib_time)
