from flask import render_template, url_for, Blueprint, redirect, flash
from flask_login import logout_user, login_user, login_required, current_user
from poultry_manager.forms import RegisterForm, LoginForm
from poultry_manager import db
from poultry_manager.models.user import User, RoleEnum
from poultry_manager.middleware.access_control import admin_required, worker_required

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/home')
def home_page():
    """
        Render the home page. Redirect authenticated users to the tasks page.
        """
    if current_user.is_authenticated:
        return redirect(url_for('main.inventory_page'))
    return render_template('home.html')


@bp.route('/register-account', methods=['GET', 'POST'])
def register_page():
    """
        Handle user registration. Create a new user if the form is valid,
        log them in, and redirect to the add task page.
        """
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account successfully created! You are logged in as: {user_to_create.username}", category='success')
        return redirect(url_for('login_page'))
    if form.errors:
        for field, err_msgs in form.errors.items():
            for err_msg in err_msgs:
                flash(f"There was an error with {field}: {err_msg}", category='danger')

    return render_template('register.html', form=form)


@bp.route('/login-user', methods=['GET', 'POST'])
def login_page():
    """
        Handle user login. Authenticate and log in the user if the form is valid.
    """
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f'Successfully logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('main.inventory_page'))
        else:
            flash('Login failed. Check your email and password.', category='danger')

    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have successfully logged out', category='info')
    return redirect(url_for('main.home_page'))


@bp.route('/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin-only dashboard showing farm data and worker management"""
    # Logic for admin dashboard
    return render_template('admin_dashboard.html')


@bp.route('/promote/<int:user_id>')
@login_required
@admin_required
def promote_user(user_id):
    """Admin promotes a worker to admin"""
    user = User.query.get(user_id)
    if user and user.is_worker():
        user.role = RoleEnum.ADMIN
        db.session.commit()
        flash(f'{user.username} has been promoted to admin.', category='success')
    else:
        flash('User not found or already an admin.', category='danger')
    return redirect(url_for('admin_dashboard'))


@bp.route('/demote/<int:user_id>')
@login_required
@admin_required
def demote_user(user_id):
    """Admin demotes an admin back to worker"""
    user = User.query.get(user_id)
    if user and user.is_admin():
        user.role = RoleEnum.WORKER
        db.session.commit()
        flash(f'{user.username} has been demoted to worker.', category='success')
    else:
        flash('User not found or already a worker.', category='danger')
    return redirect(url_for('admin_dashboard'))


@bp.route('/worker-dashboard')
@login_required
@worker_required
def worker_dashboard():
    """Worker-only dashboard to enter farm records"""
    # Logic for worker dashboard
    return render_template('worker_dashboard.html')


@bp.route('/inventory')
def inventory_page():
    # logic for inventory
    return render_template('inventory.html')


@bp.route('/health-report')
def health_page():
    # logic for health records
    return render_template('health.html')


@bp.route('/production-reports')
def production_page():
    # logic for production record
    return render_template('production.html')
