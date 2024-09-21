import unittest
from poultry_manager import db, create_app
from poultry_manager.models.flock import Flock
from poultry_manager.models.user import User


class TestFlockModel(unittest.TestCase):
    """Unit tests for the Flock model."""

    def setUp(self):
        """Set up a temporary database and Flask test environment."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a user for foreign key reference
        self.user = User(username='user1', email='user1@example.com', password='password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down the temporary database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_flock_creation(self):
        """Test that a flock can be successfully created and added to the database."""
        flock = Flock(breed='Layer', quantity=100, age=5, user_id=self.user.id)
        db.session.add(flock)
        db.session.commit()

        # Fetch the flock from the database
        created_flock = Flock.query.filter_by(breed='Layer').first()

        # Assertions
        self.assertIsNotNone(created_flock)
        self.assertEqual(created_flock.breed, 'Layer')
        self.assertEqual(created_flock.quantity, 100)
        self.assertEqual(created_flock.age, 5)
        self.assertEqual(created_flock.user_id, self.user.id)

    def test_flock_deaths_and_sold_defaults(self):
        """Test that deaths and sold fields default to 0."""
        flock = Flock(breed='Broiler', quantity=150, age=6, user_id=self.user.id)
        db.session.add(flock)
        db.session.commit()

        # Fetch the flock from the database
        created_flock = Flock.query.filter_by(breed='Broiler').first()

        # Assertions
        self.assertEqual(created_flock.deaths, 0)
        self.assertEqual(created_flock.sold, 0)

    def test_flock_repr(self):
        """Test the string representation of the flock."""
        flock = Flock(breed='Free Range', quantity=200, age=8, user_id=self.user.id)
        self.assertEqual(repr(flock), "<Flock Free Range (200 chickens), 8 weeks old>")


if __name__ == '__main__':
    unittest.main()
