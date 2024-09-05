from datetime import datetime
from . import db, bcrypt
from enum import Enum


# Model for different roles
class RoleEnum(Enum):
    FARMER = 'farmer'
    ADMIN = 'admin'


# User Model
class User(db.Model):
    """ Class to represent the users table """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.FARMER)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farms = db.relationship('Farm', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

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
        return f'<User {self.username}, {self.email}>'

    @staticmethod
    def validate_role(role):
        """Validates the role against allowed roles."""
        if not isinstance(role, RoleEnum):
            raise ValueError(f"Invalid role: {role}")

    # Method to retrieve all farm owned by a user
    def get_farms(self):
        """Returns all farms owned by the user."""
        return self.farms.all()


# Farm Model
class Farm(db.Model):
    """ Class to represent table for a poultry with many farms """
    __tablename__ = 'farms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Relationships
    inventory = db.relationship('Inventory', backref='farm', lazy=True, cascade="all, delete-orphan")
    productions = db.relationship('Production', backref='farm', lazy=True, cascade="all, delete-orphan")
    health_records = db.relationship('HealthRecord', backref='farm', lazy=True, cascade="all, delete-orphan")
    flocks = db.relationship('Flock', backref='farm', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        """String representation of the farm object."""
        return f"<Farm {self.name} in {self.location}>"

    # Method to calculate all chicken in a farm
    def total_chickens(self):
        """Returns the total number of chickens across all flocks in the farm."""
        return sum(flock.quantity for flock in self.flocks)

    # Method to calculate total chickens of a specific breed in a farm
    def total_chickens_by_breed(self, breed_name):
        """Returns the total number of chickens for a particular breed in the farm."""
        return sum(flock.quantity for flock in self.flocks if flock.breed.lower() == breed_name.lower())


# Flock Model
class Flock(db.Model):
    """ Class to represent the flock table"""
    __tablename__ = 'flocks'

    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    age_weeks = db.Column(db.Integer, nullable=False)

    # Foreign Key
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False, index=True)

    # Relationships
    production_records = db.relationship('Production', backref='flock', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Flock {self.breed} ({self.quantity} chickens), {self.age_weeks} weeks old>"

    # Method to calculate average age of chickens
    def average_age(self):
        """Returns the average age of the flock."""
        return self.age_weeks

    # Class method to get all chickens of a breed in the farms
    @classmethod
    def total_chickens_by_breed(cls, breed_name):
        """Returns the total number of chickens for a particular breed across all farms."""
        return db.session.query(db.func.sum(cls.quantity)).filter(cls.breed.ilike(breed_name)).scalar() or 0


# Inventory Model
class Inventory(db.Model):
    """" Class to represent the inventory table of the farm """
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    purchase_order_number = db.Column(db.String(100), nullable=True)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign Key
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False, index=True)

    # Unique constraint considering multiple purchases
    __table_args__ = (
        db.UniqueConstraint('farm_id', 'item_name', 'purchase_date', name='unique_inventory_entry'),
    )

    def __repr__(self):
        """String representation of the inventory item."""
        return f'<Inventory {self.item_name}, Quantity: {self.quantity} {self.unit}>'


# Production Record Model
class Production(db.Model):
    """ Class to represent the production table """
    __tablename__ = 'production'

    id = db.Column(db.Integer, primary_key=True)
    eggs_collected = db.Column(db.Integer, nullable=False)
    date_collected = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign key
    flock_id = db.Column(db.Integer, db.ForeignKey('flocks.id'), nullable=False, index=True)

    def __repr__(self):
        """String representation of the production record."""
        return f"<Production Record Date: {self.date_collected}, Eggs: {self.eggs_collected}>"


# Health Record Model
class HealthRecord(db.Model):
    """Class to represent the health records table."""
    __tablename__ = 'health_records'

    id = db.Column(db.Integer, primary_key=True)
    health_status = db.Column(db.String(200), nullable=False)
    health_issue = db.Column(db.String(200), nullable=False)
    medication_given = db.Column(db.String(200), nullable=False)
    date_reported = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign Key
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False, index=True)

    def __repr__(self):
        """String representation of the health record."""
        return f'<Health Record Date: {self.date_reported}, Status: {self.health_status}>'
