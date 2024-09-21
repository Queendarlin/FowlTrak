import unittest
from poultry_manager import db, create_app
from poultry_manager.models.user import User, RoleEnum


class TestUserModel(unittest.TestCase):
    """Unit tests for the User model."""

    def setUp(self):
        """
        Set up a temporary database and Flask test environment.
        """
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Tear down the temporary database.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """
        Test that a user can be successfully created and added to the database.
        """
        user = User(username='john_doe', email='john@example.com', password='password123')
        db.session.add(user)
        db.session.commit()

        # Fetch the user from the database
        created_user = User.query.filter_by(email='john@example.com').first()

        # Assertions
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, 'john_doe')
        self.assertEqual(created_user.email, 'john@example.com')

    def test_password_is_hashed(self):
        """
        Test that the password is hashed and not stored in plain text.
        """
        user = User(username='jane_doe', email='jane@example.com', password='securepassword')
        db.session.add(user)
        db.session.commit()

        # Fetch the user from the database
        created_user = User.query.filter_by(email='jane@example.com').first()

        # Ensure password_hash is not None and password is not accessible directly
        self.assertIsNotNone(created_user.password_hash)
        with self.assertRaises(AttributeError):
            _ = created_user.password

    def test_check_password(self):
        """
        Test the check_password method to ensure it correctly verifies the password.
        """
        user = User(username='jane_doe', email='jane@example.com', password='mypassword')
        db.session.add(user)
        db.session.commit()

        # Fetch the user and check password
        created_user = User.query.filter_by(email='jane@example.com').first()

        self.assertTrue(created_user.check_password('mypassword'))
        self.assertFalse(created_user.check_password('wrongpassword'))

    def test_role_validation(self):
        """
        Test that an invalid role raises a ValueError.
        """
        user = User(username='admin_user', email='admin@example.com', password='adminpassword')

        # Test valid role
        user.role = RoleEnum.ADMIN
        self.assertEqual(user.role, RoleEnum.ADMIN)

        # Test invalid role
        with self.assertRaises(ValueError):
            User.validate_role('invalid_role')


if __name__ == '__main__':
    unittest.main()
