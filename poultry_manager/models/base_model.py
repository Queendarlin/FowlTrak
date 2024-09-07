# Base model

from poultry_manager import db
from poultry_manager.live_time import NetworkTime


ntplib_time = NetworkTime.network_time()


class BaseModel(db.Model):
    """ Base model to include created_at and updated_at fields """
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    updated_at = db.Column(db.DateTime(), nullable=False, default=ntplib_time, onupdate=ntplib_time)
