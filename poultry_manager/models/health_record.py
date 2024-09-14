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

    @staticmethod
    def total_sick_birds():
        """Returns the total number of sick birds across all records."""
        return db.session.query(db.func.sum(HealthRecord.number_sick)).scalar()

    @staticmethod
    def sick_count_in_period(start_date, end_date):
        """Returns the total number of sick birds reported within a specific date range."""
        return db.session.query(db.func.sum(HealthRecord.number_sick)).filter(
            HealthRecord.date_reported.between(start_date, end_date)
        ).scalar()

    @staticmethod
    def most_common_symptoms(limit=10):
        """Returns the most common symptoms reported, limited to a specified number."""
        result = db.session.query(
            HealthRecord.symptom,
            db.func.count(HealthRecord.symptom).label('count')
        ).group_by(HealthRecord.symptom).order_by(db.desc('count')).limit(limit).all()
        return result

    @staticmethod
    def medication_given_summary():
        """Returns a summary of medications given, including their frequencies."""
        result = db.session.query(
            HealthRecord.medication_given,
            db.func.count(HealthRecord.medication_given).label('count')
        ).group_by(HealthRecord.medication_given).all()
        return result

    @staticmethod
    def health_records_by_date(date):
        """Returns all health records for a specific date."""
        return HealthRecord.query.filter(db.func.date(HealthRecord.date_reported) == date).all()

    def __repr__(self):
        """String representation of the health record."""
        return f'<Health Record Date: {self.date_reported}, Status: {self.health_status}>'
