# Inventory Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time


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
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship
    user = db.relationship('User', back_populates='inventories', lazy=True)

    # Unique constraint considering multiple purchases
    __table_args__ = (
        db.UniqueConstraint('item_name', 'purchase_date', name='unique_inventory_entry'),
    )

    # Method to calculate total inventory by category (Equipment, Supplies)
    @staticmethod
    def total_by_category(category):
        """Returns total inventory for a specific category in the farm."""
        return db.session.query(db.func.sum(Inventory.quantity)).filter_by(category=category).scalar()

    # Method to calculate total cost of all items
    @staticmethod
    def total_inventory_cost():
        """Returns the total cost of all items in the inventory."""
        return db.session.query(db.func.sum(Inventory.quantity * Inventory.cost)).scalar()

    @staticmethod
    def items_by_category(category):
        """Returns all inventory items for a specific category."""
        return Inventory.query.filter_by(category=category).all()

    @staticmethod
    def total_quantity():
        """Returns the total quantity of all items in the inventory."""
        return db.session.query(db.func.sum(Inventory.quantity)).scalar()

    @staticmethod
    def total_by_item_name(item_name):
        """Returns the total quantity of a specific item by name."""
        return db.session.query(db.func.sum(Inventory.quantity)).filter_by(item_name=item_name).scalar()

    @staticmethod
    def inventory_summary_by_date_range(start_date, end_date):
        """Returns a summary of inventory items added within a specific date range."""
        return Inventory.query.filter(
            Inventory.purchase_date.between(start_date, end_date)
        ).all()

    @staticmethod
    def recent_purchases(limit=10):
        """Returns the most recent purchases based on purchase date."""
        return Inventory.query.order_by(Inventory.purchase_date.desc()).limit(limit).all()

    @staticmethod
    def inventory_items_summary():
        """Returns a summary of all inventory items with total quantity and cost."""
        results = db.session.query(
            Inventory.item_name,
            db.func.sum(Inventory.quantity).label('total_quantity'),
            db.func.sum(Inventory.quantity * Inventory.cost).label('total_cost')
        ).group_by(Inventory.item_name).all()
        return results

    def __repr__(self):
        """String representation of the inventory item."""
        return f'<Inventory {self.item_name}, Quantity: {self.quantity} {self.unit}, Cost: {self.cost}>'
