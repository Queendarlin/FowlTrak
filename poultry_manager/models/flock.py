# Flock Model

from poultry_manager import db
from .base_model import BaseModel


class Flock(BaseModel):
    """ Class to represent the flock table"""
    __tablename__ = 'flocks'

    breed = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    deaths = db.Column(db.Integer(), default=0)
    sold = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return f"<Flock {self.breed} ({self.quantity} chickens), {self.age_weeks} weeks old>"

    # Method to calculate mortality rate for this flock
    def mortality_rate(self):
        """Calculates the mortality rate for the flock."""
        return (self.deaths / self.quantity) * 100 if self.quantity > 0 else 0
