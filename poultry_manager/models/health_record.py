# Health Record Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class HealthRecord(BaseModel):
    """Class to represent the health records table."""
    __tablename__ = 'health_records'

    health_status = db.Column(db.String(200), nullable=False)
    health_issue = db.Column(db.String(200), nullable=False)
    medication_given = db.Column(db.String(200), nullable=False)
    date_reported = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    vaccinated = db.Column(db.Boolean(), default=False)
    vaccination_date = db.Column(db.DateTime(), nullable=True)

    # Foreign Key
    farm_id = db.Column(db.Integer(), db.ForeignKey('farms.id'), nullable=False, index=True)

    def __repr__(self):
        """String representation of the health record."""
        return f'<Health Record Date: {self.date_reported}, Status: {self.health_status}>'
