"""
Production Model for Flask-SQLAlchemy

This module defines the `Production` class, which represents records of egg production
in the farm's database.
It inherits from `BaseModel` and includes fields relevant to egg production tracking.

Dependencies:
- `db`: SQLAlchemy database instance from `poultry_manager`.
- `BaseModel`: Abstract base class providing common fields, including timestamps.

Usage:
To use this model, you need to define the `User` model with a `productions`
relationship that corresponds to this model.

"""

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class Production(BaseModel):
    """
    Model class to represent egg production records in the farm's database.

    Attributes:
        id (int): Primary key of the model, inherited from `BaseModel`.
        number_eggs_collected (int): Number of eggs collected on a specific date.
        eggs_sold (int): Number of eggs sold, default is 0.
        date_collected (datetime): The date when the eggs were collected,
                                    default is the current network time.
        user_id (int): Foreign key to the `User` table, must be provided.
        user (User): Relationship to the `User` model indicating the user who recorded the production.

    Methods:
        __repr__: Returns a string representation of the production record,
        including the date and number of eggs collected.
    """
    __tablename__ = 'production'

    number_eggs_collected = db.Column(db.Integer(), nullable=False)
    eggs_sold = db.Column(db.Integer(), default=0)
    date_collected = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    created_by_username = db.Column(db.String(100))

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Define relationship with User model
    user = db.relationship('User', back_populates='productions')

    def __repr__(self):
        """String representation of the production record."""
        return f"<Production Record Date: {self.date_collected}, Eggs: {self.number_eggs_collected}>"
