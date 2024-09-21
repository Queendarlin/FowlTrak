import unittest
from poultry_manager import db, create_app
from poultry_manager.models.production import Production


class TestProductionModel(unittest.TestCase):
    """Unit tests for the Production model."""

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

    def test_production_creation(self):
        """Test that a production record can be successfully created and added to the database."""
        production_record = Production(
            number_eggs_collected=50,
            eggs_sold=20
        )
        db.session.add(production_record)
        db.session.commit()

        # Fetch the production record from the database
        created_record = Production.query.filter_by(number_eggs_collected=50).first()

        # Assertions
        self.assertIsNotNone(created_record)
        self.assertEqual(created_record.number_eggs_collected, 50)
        self.assertEqual(created_record.eggs_sold, 20)

    def test_production_repr(self):
        """Test the __repr__ method of the Production model."""
        production_record = Production(
            number_eggs_collected=50
        )
        db.session.add(production_record)
        db.session.commit()

        # Fetch the production record from the database
        created_record = Production.query.filter_by(number_eggs_collected=50).first()

        # Assertions
        self.assertEqual(
            repr(created_record),
            f"<Production Record Date: {created_record.date_collected}, Eggs: {created_record.number_eggs_collected}>"
        )

    def test_default_eggs_sold(self):
        """Test that the default value for eggs_sold is 0."""
        production_record = Production(
            number_eggs_collected=50
        )
        db.session.add(production_record)
        db.session.commit()

        # Fetch the production record from the database
        created_record = Production.query.filter_by(number_eggs_collected=50).first()

        # Assertions
        self.assertEqual(created_record.eggs_sold, 0)


if __name__ == '__main__':
    unittest.main()
