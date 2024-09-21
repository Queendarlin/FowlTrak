"""
This module promotes a user to admin status in the FowlTrak application.

It initializes the Flask application, loads environment variables,
and provides a function to promote a specified user to admin.

Usage:
    Run this module directly to promote a user to admin:
        python <module_name>.py
"""

import os
from poultry_manager import create_app, db
from poultry_manager.models.user import User, RoleEnum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = create_app()


def promote_to_admin(username):
    """
        Promote a user to admin status.

        Args:
            username (str): The username of the user to be promoted.

        If the user exists and is currently a worker, their role will be updated
        to admin. If the user does not exist or is already an admin,
        appropriate messages will be printed.

        Returns:
            None
    """
    with app.app_context():
        # Find the user by username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and if they are a worker
        if not user:
            print(f"User '{username}' not found.")
            return

        if user.role == RoleEnum.ADMIN:
            print(f"User '{username}' is already an admin.")
            return

        # Promote the user to admin
        user.role = RoleEnum.ADMIN
        db.session.commit()
        print(f"User '{username}' has been promoted to admin.")


if __name__ == "__main__":
    # Pass the username of the user to be promoted as an environment variable
    owner_username = os.getenv('OWNER_USERNAME', 'farm_owner')

    promote_to_admin(owner_username)
