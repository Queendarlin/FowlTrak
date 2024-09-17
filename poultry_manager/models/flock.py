"""
Flock Model for Flask-SQLAlchemy

This module defines the `Flock` class, which represents a flock of chickens in the database.
It inherits from `BaseModel` and includes additional fields specific to flocks.

Dependencies:
- `db`: SQLAlchemy database instance from `poultry_manager`.
- `BaseModel`: Abstract base class providing common fields, including timestamps.

Usage:
To use this model, you need to define the `User` model with a `flocks` relationship that corresponds to this model.

"""

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class Flock(BaseModel):
    """
    Model class to represent a flock of chickens in the database.

    Attributes:
        id (int): Primary key of the model, inherited from `BaseModel`.
        breed (str): The breed of the chickens, must be provided (string, 50 characters).
        quantity (int): The number of chickens in the flock, must be provided.
        age (int): The age of the chickens in weeks, must be provided.
        deaths (int): Number of chickens that have died, default is 0.
        sold (int): Number of chickens that have been sold, default is 0.
        entry_date (datetime): The date when the flock was entered into the system, default is the current network time.
        user_id (int): Foreign key to the `User` table, must be provided.
        user (User): Relationship to the `User` model indicating the owner of the flock.

    Methods:
        __repr__: Returns a string representation of the flock with breed, quantity, and age in weeks.
    """
    __tablename__ = 'flocks'

    breed = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    deaths = db.Column(db.Integer(), default=0)
    sold = db.Column(db.Integer(), default=0)
    entry_date = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    created_by_username = db.Column(db.String(100))

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Define relationship with User model
    user = db.relationship('User', back_populates='flocks')

    def __repr__(self):
        """ String representation of the flock with breed, quantity, and age in weeks """
        return f"<Flock {self.breed} ({self.quantity} chickens), {self.age} weeks old>"
