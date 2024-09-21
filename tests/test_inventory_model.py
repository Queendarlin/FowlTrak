import unittest
from poultry_manager import db, create_app
from poultry_manager.models.inventory import Inventory


class TestInventoryModel(unittest.TestCase):
    """Unit tests for the Inventory model."""

    def setUp(self):
        """Set up a temporary database and Flask test environment."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down the temporary database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_inventory_creation(self):
        """Test that an inventory item can be successfully created and added to the database."""
        inventory_item = Inventory(
            item_name='Chicken Feed',
            category='Feed',
            quantity=100,
            unit='kg',
            cost=25.50,
            purchase_order_number='PO12345'
        )
        db.session.add(inventory_item)
        db.session.commit()

        # Fetch the inventory item from the database
        created_item = Inventory.query.filter_by(item_name='Chicken Feed').first()

        # Assertions
        self.assertIsNotNone(created_item)
        self.assertEqual(created_item.item_name, 'Chicken Feed')
        self.assertEqual(created_item.quantity, 100)
        self.assertEqual(created_item.unit, 'kg')
        self.assertEqual(created_item.cost, 25.50)

    def test_inventory_repr(self):
        """Test the __repr__ method of the Inventory model."""
        inventory_item = Inventory(
            item_name='Chicken Feed',
            category='Feed',
            quantity=100,
            unit='kg',
            cost=25.50
        )
        db.session.add(inventory_item)
        db.session.commit()

        # Fetch the inventory item from the database
        created_item = Inventory.query.filter_by(item_name='Chicken Feed').first()

        # Assertions
        self.assertEqual(
            repr(created_item),
            '<Inventory Chicken Feed, Quantity: 100 kg, Cost: 25.5>'
        )


if __name__ == '__main__':
    unittest.main()
