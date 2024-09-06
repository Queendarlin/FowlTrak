# Inventory Model

from poultry_manager import db
from .base_model import BaseModel, ntplib_time
from sqlalchemy.dialects.postgresql import UUID


class Inventory(BaseModel):
    """" Class to represent the inventory table of the farm """
    __tablename__ = 'inventory'

    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    quantity = db.Column(db.Integer(), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float(), nullable=False)
    purchase_order_number = db.Column(db.String(100), nullable=True)
    purchase_date = db.Column(db.DateTime(), nullable=False, default=ntplib_time)

    # Foreign Key
    farm_id = db.Column(UUID(as_uuid=True), db.ForeignKey('farms.id'), nullable=False, index=True)

    # Unique constraint considering multiple purchases
    __table_args__ = (
        db.UniqueConstraint('farm_id', 'item_name', 'purchase_date', name='unique_inventory_entry'),
    )

    # Method to calculate total inventory by category (Feed, Equipment, Supplies)
    def total_by_category(self):
        """Returns total inventory for a specific category in the farm."""
        return db.session.query(db.func.sum(Inventory.quantity)).filter_by(farm_id=self.farm_id,
                                                                           category=self.category).scalar()

    def __repr__(self):
        """String representation of the inventory item."""
        return f'<Inventory {self.item_name}, Quantity: {self.quantity} {self.unit}, Cost: {self.cost}>'
