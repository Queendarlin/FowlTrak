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

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define relationship with User model
    user = db.relationship('User', back_populates='flocks')

    def __repr__(self):
        return f"<Flock {self.breed} ({self.quantity} chickens), {self.age_weeks} weeks old>"

    # Method to calculate mortality rate for this flock
    def mortality_rate(self):
        """Calculates the mortality rate for the flock."""
        return (self.deaths / self.quantity) * 100 if self.quantity > 0 else 0

    @staticmethod
    def total_birds():
        return db.session.query(db.func.sum(Flock.quantity)).scalar()

    @staticmethod
    def birds_sold_in_period(start_date, end_date):
        return db.session.query(db.func.sum(Flock.sold)).filter(Flock.date.between(start_date, end_date)).scalar()

    @staticmethod
    def deaths_in_period(start_date, end_date):
        return db.session.query(db.func.sum(Flock.deaths)).filter(Flock.date >= start_date,
                                                                  Flock.date <= end_date).scalar()
