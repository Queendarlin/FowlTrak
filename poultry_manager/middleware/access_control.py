# Role Based Access Control
from functools import wraps
from flask import abort
from flask_login import current_user


# Decorator to restrict access to only admins
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function


# Decorator to restrict access to workers
def worker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_worker():
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function


# Decorator to restrict access to admins and workers
def admin_or_worker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (current_user.is_admin() or current_user.is_worker()):
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function
