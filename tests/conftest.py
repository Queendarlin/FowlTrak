import pytest
from poultry_manager import create_app, db
from sqlalchemy.orm import scoped_session, sessionmaker
from .config_test import TestConfig


@pytest.fixture(scope='module')
def app():
    """Set up the Flask application for testing."""
    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        db.create_all()  # Create test database tables
        yield app  # Run tests
        db.drop_all()  # Teardown after tests


@pytest.fixture(scope='function')
def session(app):
    """Create a new database session for a test."""
    # Create a new connection and transaction for each test
    connection = db.engine.connect()
    transaction = connection.begin()

    # Create a scoped session using the connection
    session_factory = sessionmaker(bind=connection)
    scoped_session_factory = scoped_session(session_factory)

    # Bind the session to the db object
    db.session = scoped_session_factory()

    yield db.session  # This is where the testing happens

    # Cleanup
    db.session.remove()  # Correctly remove the scoped session
    transaction.rollback()
    connection.close()
