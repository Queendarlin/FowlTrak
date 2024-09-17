"""
HealthRecord Model for Flask-SQLAlchemy

This module defines the `HealthRecord` class, which represents health records for flocks in the database.
It inherits from `BaseModel` and includes fields specific to health records.

Dependencies:
- `db`: SQLAlchemy database instance from `poultry_manager`.
- `BaseModel`: Abstract base class providing common fields, including timestamps.

Usage:
To use this model, you need to define the `User` model with a `health_records` relationship that corresponds to this model.

"""

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class HealthRecord(BaseModel):
    """
    Model class to represent health records of flocks in the database.

    Attributes:
        id (int): Primary key of the model, inherited from `BaseModel`.
        number_sick (int): The number of sick chickens, optional.
        symptom (str): Description of symptoms observed (string, 200 characters).
        medication_given (str): Description of the medication administered (string, 200 characters).
        date_reported (datetime): The date when the health issue was reported, default is the current network time.
        user_id (int): Foreign key to the `User` table, must be provided.
        user (User): Relationship to the `User` model indicating the user who reported the health record.

    Methods:
        __repr__: Returns a string representation of the health record with report date and status.
    """
    __tablename__ = 'health_records'

    number_sick = db.Column(db.Integer, nullable=True)
    symptom = db.Column(db.String(200), nullable=False)
    medication_given = db.Column(db.String(200), nullable=False)
    date_reported = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    created_by_username = db.Column(db.String(100))

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Define relationship with User model
    user = db.relationship('User', back_populates='health_records')

    def __repr__(self):
        """String representation of the health record."""
        return f'<Health Record Date: {self.date_reported}, Symptoms: {self.symptom}>'
