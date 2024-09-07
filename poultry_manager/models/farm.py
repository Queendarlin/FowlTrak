# Farm Model

from poultry_manager import db
from .base_model import BaseModel


class Farm(BaseModel):
    """ Class to represent table for a poultry with many farms """
    __tablename__ = 'farms'

    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False, index=True)

    # Foreign Key
    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False, index=True)

    # Relationships
    inventory = db.relationship('Inventory', backref='farm', lazy=True, cascade="all, delete-orphan")
    productions = db.relationship('Production', backref='farm', lazy=True, cascade="all, delete-orphan")
    health_records = db.relationship('HealthRecord', backref='farm', lazy=True, cascade="all, delete-orphan")
    flocks = db.relationship('Flock', backref='farm', lazy=True, cascade="all, delete-orphan")

    # Method to calculate all chicken in a farm
    def total_chickens(self):
        """Returns the total number of chickens across all flocks in the farm."""
        return sum(flock.quantity for flock in self.flocks)

    # Method to calculate total chickens of a specific breed in a farm
    def total_chickens_by_breed(self, breed_name):
        """Returns the total number of chickens for a particular breed in the farm."""
        return sum(flock.quantity for flock in self.flocks if flock.breed.lower() == breed_name.lower())

    # Egg production methods
    def total_eggs_collected(self):
        """Returns the total number of eggs collected in the farm."""
        return sum(prod.eggs_collected for prod in self.productions)

    def eggs_collected_by_date(self, date):
        """Returns the number of eggs collected on a specific date."""
        return sum(prod.eggs_collected for prod in self.productions if prod.date_collected.date() == date)

    # Mortality rate method (tracks total chicken deaths)
    def calculate_mortality_rate(self):
        """Calculates the weekly or monthly mortality rate."""
        deaths = sum(flock.deaths for flock in self.flocks)
        total_alive = self.total_chickens()
        return (deaths / (deaths + total_alive)) * 100 if deaths + total_alive > 0 else 0

    def __repr__(self):
        """String representation of the farm object."""
        return f"<Farm {self.name} in {self.location}>"
