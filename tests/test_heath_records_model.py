import unittest
from poultry_manager import db, create_app
from poultry_manager.models.health_record import HealthRecord
from poultry_manager.models.user import User


class TestHealthRecordModel(unittest.TestCase):
    """Unit tests for the HealthRecord model."""

    def setUp(self):
        """Set up a temporary database and Flask test environment."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a user for testing
        self.user = User(username='test_user', email='test@example.com', password='password123')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down the temporary database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_health_record_creation(self):
        """Test that a health record can be successfully created and added to the database."""
        health_record = HealthRecord(
            number_sick=5,
            symptom='Coughing',
            medication_given='Antibiotic',
            user_id=self.user.id
        )
        db.session.add(health_record)
        db.session.commit()

        # Fetch the health record from the database
        created_record = HealthRecord.query.filter_by(symptom='Coughing').first()

        # Assertions
        self.assertIsNotNone(created_record)
        self.assertEqual(created_record.number_sick, 5)
        self.assertEqual(created_record.symptom, 'Coughing')
        self.assertEqual(created_record.medication_given, 'Antibiotic')

    def test_health_record_repr(self):
        """Test the __repr__ method of the HealthRecord."""
        health_record = HealthRecord(
            number_sick=3,
            symptom='Lethargy',
            medication_given='Vitamins',
            user_id=self.user.id
        )
        db.session.add(health_record)
        db.session.commit()

        self.assertEqual(repr(health_record),
                         f'<Health Record Date: {health_record.date_reported}, Symptoms: Lethargy>')


if __name__ == '__main__':
    unittest.main()
