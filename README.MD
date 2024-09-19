# FowlTrak - Poultry Management System
A comprehensive web-based solution for efficient poultry farm management, built with Flask, SQLAlchemy, and other powerful tools. Manage your flock, production records, health logs, inventory, and more, all from a user-friendly dashboard.

Deployed Site: https://fowltrak.onrender.com/

Live Demo: (https://www.youtube.com/watch?v=r3BL019G3tM)

Author LinkedIn: [Queendarlin Nnamani](https://www.linkedin.com/in/queendarlin-nnamani/)

## Table of Contents
* Introduction
* Tech Stack
* Installation
* Usage
* Features
* Contributing
* Related Projects
* License

## Introduction
FowlTrak is a dynamic platform tailored for poultry farm managers to streamline daily operations. This application provides a seamless way to track and manage flocks, production metrics, health records, and inventory, helping improve productivity and optimize resources. Built with a robust backend using Flask and SQLAlchemy, it ensures secure data management while offering a clean, intuitive user interface.


## Tech Stack
Backend:

* Python (Flask framework)
* SQLAlchemy (ORM)
* Flask-Migrate (Database migrations)
* Flask-Bcrypt (Password hashing)
* Flask-Login (User session management)

Frontend:

* HTML5, CSS3 (Bootstrap 5.3 for UI components)
* JavaScript (AJAX for dynamic content)

Database:

* PostgreSQL

Hosting and Deployment:

* [Render](https://render.com/) (Deployed on Render platform)

## Installation
To run FowlTrak locally, follow these steps:

1. Clone the Repository:
```
git clone https://github.com/Queendarlin/FowlTrak.git
cd FowlTrak
```

2. Set Up Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

3. Install Dependencies:
```
pip install -r requirements.txt
```

4. Set Up Environment Variables: Create a .env file in the project root and add the following:
```
SECRET_KEY=your_secret_key
DATABASE_URL=your_postgresql_url # or your choice of database
```

5. Run Migrations:
```
flask db upgrade
```

6. Run the Application:
```
python app.py
```

## Usage
* Promote User to Admin
FowlTrak allows a farm owner (or admin) to be promoted using the following script. Ensure you’ve set the OWNER_USERNAME in your .env file.

Run the script:
```
python promote_to_admin.py
```

## Features
* Flock Management: Track flock details, add new birds, and monitor the number of flocks.

* Production Records: Log egg production and sales.

* Health Monitoring: Record and manage health issues.

* Inventory Management: Track feed, equipment, utilities, and other farm supplies.

* User Roles: Different access levels for workers and administrators.

* Responsive Design: Fully responsive, making it accessible on mobile and tablet devices.

## Contributing
Contributions to FowlTrak are welcome! Here’s how you can help:

* Fork the repository.

* Create a feature branch (git checkout -b feature-branch-name).

* Commit your changes (git commit -am 'Add new feature').

* Push to the branch (git push origin feature-branch-name).

* Open a Pull Request.

**Before contributing, please ensure your changes align with the project's architecture and guidelines.**


## License
FowlTrak is licensed under the MIT License. See the LICENSE file for more details.

Thank you for checking out FowlTrak! If you have any questions or suggestions, feel free to reach out via LinkedIn or open an issue on GitHub.