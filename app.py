"""
This module initializes and runs the Fowltrak application.

It imports the `create_app` function from the `poultry_manager` module,
creates an application instance, and starts the server in debug mode when executed directly.

Usage:
    Run this module directly to start the application:
        python <module_name>.py
"""

from poultry_manager import create_app

# Create an instance of the Flask application
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
