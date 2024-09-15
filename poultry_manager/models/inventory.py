# Inventory Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time
from datetime import datetime, timedelta


class Inventory(BaseModel):
    """" Class to represent the inventory table of the farm """
    __tablename__ = 'inventory'

    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    quantity = db.Column(db.Integer(), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float(), nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='USD')
    purchase_order_number = db.Column(db.String(100), nullable=True)
    purchase_date = db.Column(db.DateTime(), nullable=False, default=ntplib_time)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship
    user = db.relationship('User', back_populates='inventories', lazy=True)

    # Unique constraint considering multiple purchases
    __table_args__ = (
        db.UniqueConstraint('item_name', 'purchase_date', name='unique_inventory_entry'),
    )

    def __repr__(self):
        """String representation of the inventory item."""
        return f'<Inventory {self.item_name}, Quantity: {self.quantity} {self.unit}, Cost: {self.cost}>'
