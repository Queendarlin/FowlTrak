# poultry_manager/models/__init__.py

from .base_model import BaseModel
from .user import User
from .farm import Farm
from .flock import Flock
from .production import Production
from .health_record import HealthRecord
from .inventory import Inventory

# List all the models to be used by the application
__all__ = ['BaseModel', 'User', 'Farm', 'Flock', 'Production', 'HealthRecord', 'Inventory']
