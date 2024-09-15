# Flock Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class Flock(BaseModel):
    """ Class to represent the flock table"""
    __tablename__ = 'flocks'

    breed = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    deaths = db.Column(db.Integer(), default=0)
    sold = db.Column(db.Integer(), default=0)
    entry_date = db.Column(db.DateTime(), nullable=False, default=ntplib_time)

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define relationship with User model
    user = db.relationship('User', back_populates='flocks')

    def __repr__(self):
        return f"<Flock {self.breed} ({self.quantity} chickens), {self.age_weeks} weeks old>"
