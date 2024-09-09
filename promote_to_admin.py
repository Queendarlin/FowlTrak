import os
from flask import Flask
from poultry_manager import create_app, db
from poultry_manager.models.user import User, RoleEnum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = create_app()


def promote_to_admin(username):
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
