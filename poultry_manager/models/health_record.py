# Health Record Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class HealthRecord(BaseModel):
    """Class to represent the health records table."""
    __tablename__ = 'health_records'

    number_sick = db.Column(db.Integer, nullable=True)
    symptom = db.Column(db.String(200), nullable=False)
    medication_given = db.Column(db.String(200), nullable=False)
    date_reported = db.Column(db.DateTime(), nullable=False, default=ntplib_time)

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define relationship with User model
    user = db.relationship('User', back_populates='health_records')

    def __repr__(self):
        """String representation of the health record."""
        return f'<Health Record Date: {self.date_reported}, Status: {self.health_status}>'
