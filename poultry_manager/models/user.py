# User Model

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


# Model for different roles
class RoleEnum(Enum):
    WORKER = 'worker'
    ADMIN = 'admin'


class User(BaseModel, UserMixin):
    """ Class to represent the users table """
    __tablename__ = 'users'

    username = db.Column(db.String(length=50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.WORKER, index=True)

    # Relationships
    farms = db.relationship('Farm', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

        # Validate password
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks the hashed password against the provided password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        """ String representation of the user object"""
        return f'<User {self.email}>'

    @staticmethod
    def validate_role(role):
        """Validates the role against allowed roles."""
        if not isinstance(role, RoleEnum):
            raise ValueError(f"Invalid role: {role}")

    # Method to retrieve all farm owned by a user
    def get_farms(self):
        """Returns all farms owned by the user."""
        return self.farms.all()
