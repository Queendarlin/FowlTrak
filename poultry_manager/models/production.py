# Production Record Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time
from sqlalchemy.dialects.postgresql import UUID


class Production(BaseModel):
    """ Class to represent the production table """
    __tablename__ = 'production'

    eggs_collected = db.Column(db.Integer(), nullable=False)
    eggs_sold = db.Column(db.Integer(), default=0)
    date_collected = db.Column(db.DateTime(), nullable=False, default=ntplib_time)

    # Foreign key
    farm_id = db.Column(UUID(as_uuid=True), db.ForeignKey('farms.id'), nullable=False, index=True)
    flock_id = db.Column(UUID(as_uuid=True), db.ForeignKey('flocks.id'), nullable=False, index=True)

    def __repr__(self):
        """String representation of the production record."""
        return f"<Production Record Date: {self.date_collected}, Eggs: {self.eggs_collected}>"
