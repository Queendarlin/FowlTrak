# Production Record Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class Production(BaseModel):
    """ Class to represent the production table """
    __tablename__ = 'production'

    number_eggs_collected = db.Column(db.Integer(), nullable=False)
    eggs_sold = db.Column(db.Integer(), default=0)
    date_collected = db.Column(db.DateTime(), nullable=False, default=ntplib_time)

    # Foreign key to User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define relationship with User model
    user = db.relationship('User', back_populates='productions')

    @staticmethod
    def total_eggs_collected():
        """Returns the total number of eggs collected across all records."""
        return db.session.query(db.func.sum(Production.number_eggs_collected)).scalar()

    @staticmethod
    def total_eggs_sold():
        """Returns the total number of eggs sold across all records."""
        return db.session.query(db.func.sum(Production.eggs_sold)).scalar()

    @staticmethod
    def total_eggs_remaining():
        """Returns the total number of eggs remaining (collected - sold) across all records."""
        return db.session.query(
            db.func.sum(Production.number_eggs_collected) - db.func.sum(Production.eggs_sold)
        ).scalar()

    @staticmethod
    def eggs_collected_in_period(start_date, end_date):
        """Returns the total number of eggs collected within a specific date range."""
        return db.session.query(db.func.sum(Production.number_eggs_collected)).filter(
            Production.date_collected.between(start_date, end_date)
        ).scalar()

    @staticmethod
    def eggs_sold_in_period(start_date, end_date):
        """Returns the total number of eggs sold within a specific date range."""
        return db.session.query(db.func.sum(Production.eggs_sold)).filter(
            Production.date_collected.between(start_date, end_date)
        ).scalar()

    @staticmethod
    def production_summary_by_date(date):
        """Returns a summary of the number of eggs collected and sold on a specific date."""
        summary = db.session.query(
            db.func.sum(Production.number_eggs_collected).label('total_collected'),
            db.func.sum(Production.eggs_sold).label('total_sold')
        ).filter(
            db.func.date(Production.date_collected) == date
        ).one()
        return {
            'total_collected': summary.total_collected,
            'total_sold': summary.total_sold
        }

    def __repr__(self):
        """String representation of the production record."""
        return f"<Production Record Date: {self.date_collected}, Eggs: {self.eggs_collected}>"
