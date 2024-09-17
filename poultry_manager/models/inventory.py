"""
Inventory Model for Flask-SQLAlchemy

This module defines the `Inventory` class, which represents inventory items in the farm's inventory database.
It inherits from `BaseModel` and includes fields relevant to inventory management.

Dependencies:
- `db`: SQLAlchemy database instance from `poultry_manager`.
- `BaseModel`: Abstract base class providing common fields, including timestamps.

Usage:
To use this model, you need to define the `User` model
with an `inventories` relationship that corresponds to this model.

"""

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


class Inventory(BaseModel):
    """
    Model class to represent inventory items in the farm's inventory database.

    Attributes:
        id (int): Primary key of the model, inherited from `BaseModel`.
        item_name (str): Name of the inventory item, must be provided (string, 100 characters).
        category (str): Category of the item, must be provided and indexed (string, 50 characters).
        quantity (int): Quantity of the item in stock, must be provided.
        unit (str): Unit of measurement for the item, must be provided (string, 50 characters).
        cost (float): Cost of a single unit of the item, must be provided.
        currency (str): Currency of the cost, default is 'USD' (string, 10 characters).
        purchase_order_number (str): Optional purchase order number (string, 100 characters).
        purchase_date (datetime): The date when the item was purchased, default is the current network time.
        user_id (int): Foreign key to the `User` table, must be provided.
        user (User): Relationship to the `User` model indicating the user who manages the inventory item.

    Constraints:
        unique_inventory_entry: Ensures unique combination of item name and purchase date.

    Methods:
        __repr__: Returns a string representation of the inventory item with name, quantity, unit, and cost.
    """
    __tablename__ = 'inventory'

    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    quantity = db.Column(db.Integer(), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float(), nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='USD')
    purchase_order_number = db.Column(db.String(100), nullable=True)
    purchase_date = db.Column(db.DateTime(), nullable=False, default=ntplib_time)
    created_by_username = db.Column(db.String(100))

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Relationship
    user = db.relationship('User', back_populates='inventories', lazy=True)

    # Unique constraint considering multiple purchases
    __table_args__ = (
        db.UniqueConstraint('item_name', 'purchase_date', name='unique_inventory_entry'),
    )

    def __repr__(self):
        """String representation of the inventory item."""
        return f'<Inventory {self.item_name}, Quantity: {self.quantity} {self.unit}, Cost: {self.cost}>'
