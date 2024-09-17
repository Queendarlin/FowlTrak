"""
Role-Based Access Control (RBAC) Decorators for Flask

This module provides decorators to restrict access to routes based on the user's role.

Usage:
Apply these decorators to your route functions to enforce access control based on user roles.

"""

from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    """
    Decorator to restrict access to users with an admin role.

    Args:
        f (function): The route handler function to be decorated.

    Returns:
        function: The decorated function that restricts access based on user role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function


def worker_required(f):
    """
    Decorator to restrict access to users with a worker role.

    Args:
        f (function): The route handler function to be decorated.

    Returns:
        function: The decorated function that restricts access based on user role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_worker():
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function


def admin_or_worker_required(f):
    """
    Decorator to restrict access to users with either admin or worker roles.

    Args:
        f (function): The route handler function to be decorated.

    Returns:
        function: The decorated function that restricts access based on user role.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not (current_user.is_admin() or current_user.is_worker()):
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function
