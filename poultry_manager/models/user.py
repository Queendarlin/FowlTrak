"""
User Model for Flask-SQLAlchemy

This module defines the `User` class, which represents users in the farm's database.
It inherits from `BaseModel` and `UserMixin`, and integrates with Flask-Login for user authentication.

Dependencies:
- `db`: SQLAlchemy database instance from `poultry_manager`.
- `bcrypt`: Bcrypt instance for password hashing from `poultry_manager`.
- `UserMixin`: Flask-Login mixin for user authentication.
- `BaseModel`: Abstract base class providing common fields, including timestamps.
- `login_manager`: Flask-Login login manager for user session handling.

Usage:
To use this model, ensure that Flask-Login and Flask-Bcrypt are properly configured in your application.

"""

from poultry_manager import db, bcrypt
from enum import Enum
from flask_login import UserMixin
from .base_model import BaseModel
from poultry_manager import login_manager


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user given their user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The user object with the specified user ID.
    """
    return User.query.get(int(user_id))


# Enum class for defining user roles
class RoleEnum(Enum):
    """ Enum class defining possible user roles (`WORKER` and `ADMIN`). """
    WORKER = 'worker'
    ADMIN = 'admin'


class User(BaseModel, UserMixin):
    """
    Model class to represent users in the farm's database.

    Attributes:
        id (int): Primary key of the model, inherited from `BaseModel`.
        username (str): Username of the user, must be unique.
        email (str): Email address of the user, must be unique and indexed.
        password_hash (str): Hashed password of the user.
        role (RoleEnum): Role of the user, default is `WORKER`.
    """
    __tablename__ = 'users'

    username = db.Column(db.String(length=50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.WORKER, index=True)

    # Relationships
    inventories = db.relationship('Inventory', back_populates='user', lazy=True)
    productions = db.relationship('Production', back_populates='user', lazy=True)
    health_records = db.relationship('HealthRecord', back_populates='user', lazy=True)
    flocks = db.relationship('Flock', back_populates='user', lazy=True)

    def __init__(self, username, email, password):
        """ Initializes a new user with a hashed password. """
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        """ Property that raises an error when accessed directly, used for password hashing. """
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """ Checks the provided password against the stored hashed password. """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """String representation of the user object."""
        return f'<User {self.email}>'

    @staticmethod
    def validate_role(role):
        """Validates the role against allowed roles."""
        if not isinstance(role, RoleEnum):
            raise ValueError(f"Invalid role: {role}")

    def is_admin(self):
        """Check if the user is an admin."""
        return self.role == RoleEnum.ADMIN

    def is_worker(self):
        """Check if the user is a worker."""
        return self.role == RoleEnum.WORKER
