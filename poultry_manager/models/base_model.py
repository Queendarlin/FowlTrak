# Base model

import uuid
from poultry_manager import db
from poultry_manager.live_time import NetworkTime
from sqlalchemy.dialects.postgresql import UUID


ntplib_time = NetworkTime.network_time()


class BaseModel(db.Model):
    """ Base model to include created_at and updated_at fields """
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    updated_at = db.Column(db.DateTime(), nullable=False, default=ntplib_time, onupdate=ntplib_time)
