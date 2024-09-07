from poultry_manager.models.base_model import BaseModel
from poultry_manager import db
from poultry_manager.live_time import NetworkTime


def test_base_model_creation(session):
    """Test that a new BaseModel instance can be created and saved."""

    # Create a derived model for testing, since BaseModel is abstract
    class TestModel(BaseModel):
        __tablename__ = 'test_model'

    # Create the table for the TestModel
    db.create_all()

    # Create a new instance of TestModel
    test_instance = TestModel()
    session.add(test_instance)
    session.commit()

    # Fetch the instance from the database and assert fields
    fetched_instance = session.query(TestModel).first()
    assert fetched_instance is not None
    assert fetched_instance.id is not None
    assert fetched_instance.created_at is not None
    assert fetched_instance.updated_at is not None


def test_updated_at_changes_on_update(session):
    """Test that updated_at changes when the model is updated."""

    class TestModel(BaseModel):
        __tablename__ = 'test_model'

    db.create_all()

    # Create a new instance of TestModel
    test_instance = TestModel()
    session.add(test_instance)
    session.commit()

    # Fetch and update the instance
    fetched_instance = session.query(TestModel).first()
    original_updated_at = fetched_instance.updated_at

    # Perform an update
    fetched_instance.created_at = NetworkTime.network_time()
    session.commit()

    # Fetch the instance again and check if updated_at has changed
    updated_instance = session.query(TestModel).first()
    assert updated_instance.updated_at != original_updated_at, "updated_at should change after an update"
