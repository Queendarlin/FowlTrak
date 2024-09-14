from flask import render_template, url_for, Blueprint, redirect, flash
from flask_login import logout_user, login_user, login_required, current_user
from poultry_manager.forms import RegisterForm, LoginForm, InventoryForm, ProductionForm, FlockForm, HealthRecordForm
from poultry_manager import db
from poultry_manager.models.user import User, RoleEnum
from poultry_manager.middleware.access_control import admin_required, worker_required
from poultry_manager.models.inventory import Inventory
from poultry_manager.models.production import Production
from poultry_manager.models.flock import Flock
from poultry_manager.models.health_record import HealthRecord
from datetime import datetime, timedelta


bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/home')
def home_page():
    """
        Render the home page. Redirect authenticated users to the tasks page.
        """
    if current_user.is_authenticated:
        return redirect(url_for('main.worker_dashboard'))
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
        return redirect(url_for('main.login_page'))
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

            # Check if the user is an admin or a worker
            if attempted_user.is_admin():
                return redirect(url_for('main.admin_dashboard'))  # Redirect to admin dashboard
            elif attempted_user.is_worker():
                return redirect(url_for('main.worker_dashboard'))  # Redirect to worker dashboard
        else:
            flash('Login failed. Check your email and password.', category='danger')

    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout_page():
    """
        Log out the current user.
    """
    logout_user()
    flash('You have successfully logged out', category='info')
    return redirect(url_for('main.home_page'))


@bp.route('/workers-dashboard')
@login_required
@worker_required
def worker_dashboard():
    """
    Workers dashboard showing worker-specific options like adding inventory, viewing reports, etc.
    """
    return render_template('workers_dashboard.html', username=current_user.username, role=current_user.role.value)


@bp.route('/add_inventory', methods=['GET', 'POST'])
@worker_required
@login_required
def add_inventory():
    form = InventoryForm()
    if form.validate_on_submit():
        new_inventory = Inventory(
            item_name=form.item_name.data,
            category=form.category.data,
            quantity=form.quantity.data,
            unit=form.unit.data,
            cost=form.cost.data,
            currency=form.currency.data,
            purchase_order_number=form.purchase_order_number.data,
            user_id=current_user.id
        )
        db.session.add(new_inventory)
        db.session.commit()
        flash('Inventory item added successfully', 'success')
        return redirect(url_for('main.worker_dashboard'))
    return render_template('inventory.html', form=form)


@bp.route('/add-production', methods=['GET', 'POST'])
@login_required
@worker_required
def add_production():
    """Route to add production records."""
    form = ProductionForm()
    if form.validate_on_submit():
        # Create new production record
        production_record = Production(
            number_eggs_collected=form.number_eggs_collected.data,
            eggs_sold=form.eggs_sold.data,
            date_collected=form.date_collected.data,
            user_id=current_user.id
        )
        db.session.add(production_record)
        db.session.commit()
        flash('Production record added successfully', 'success')
        return redirect(url_for('main.worker_dashboard'))
    return render_template('production.html', form=form)


@bp.route('/add-flock', methods=['GET', 'POST'])
@login_required
@worker_required
def add_flock():
    form = FlockForm()
    if form.validate_on_submit():
        # Create a new flock record
        new_flock = Flock(
            breed=form.breed.data,
            quantity=form.quantity.data,
            age=form.age.data,
            deaths=form.deaths.data,
            sold=form.sold.data,
            user_id=current_user.id
        )
        db.session.add(new_flock)
        db.session.commit()
        flash('Flock record added successfully', 'success')
        return redirect(url_for('main.worker_dashboard'))

    return render_template('flock.html', form=form)


@bp.route('/add-health-record', methods=['GET', 'POST'])
@login_required
@worker_required
def add_health_record():
    form = HealthRecordForm()
    if form.validate_on_submit():
        health_record = HealthRecord(
            number_sick=form.number_sick.data,
            symptom=form.symptom.data,
            medication_given=form.medication_given.data,
            date_reported=form.date_reported.data,
            user_id=current_user.id
        )
        db.session.add(health_record)
        db.session.commit()
        flash('Health record added successfully', 'success')
        return redirect(url_for('main.worker_dashboard'))

    return render_template('health.html', form=form)


@bp.route('/admin-dashboard')
@login_required
@admin_required
def admin_dashboard():
    """
        Admin-only dashboard. View all records and perform management tasks.
    """
    # Fetch all data from the database
    workers = User.query.filter_by(role=RoleEnum.WORKER).all()
    inventories = Inventory.query.all()
    productions = Production.query.all()
    flocks = Flock.query.all()
    health_records = HealthRecord.query.all()

    return render_template(
        'admin_dashboard.html',
        workers=workers,
        inventories=inventories,
        productions=productions,
        flocks=flocks,
        health_records=health_records
    )


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


@bp.route('/remove-worker/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def remove_worker(user_id):
    """
    Admin removes (deletes) a worker from the system.
    """
    worker = User.query.get(user_id)

    if worker and worker.is_worker():
        db.session.delete(worker)
        db.session.commit()
        flash(f'Worker {worker.username} has been removed from the system.', category='success')
    else:
        flash('Worker not found or cannot be removed.', category='danger')

    return redirect(url_for('main.admin_dashboard'))


@bp.route('/edit-record/<model>/<int:record_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_record(model, record_id):
    """
    Admin edits a specific record based on the model.
    """
    if model == 'inventory':
        record = Inventory.query.get_or_404(record_id)
        form = InventoryForm(obj=record)
    elif model == 'production':
        record = Production.query.get_or_404(record_id)
        form = ProductionForm(obj=record)
    elif model == 'flock':
        record = Flock.query.get_or_404(record_id)
        form = FlockForm(obj=record)
    elif model == 'health_record':
        record = HealthRecord.query.get_or_404(record_id)
        form = HealthRecordForm(obj=record)
    else:
        flash('Invalid model.', 'danger')
        return redirect(url_for('main.admin_dashboard'))

    # Handle form submission
    if form.validate_on_submit():
        form.populate_obj(record)
        db.session.commit()
        flash(f'{model.capitalize()} record updated successfully.', 'success')
        return redirect(url_for('main.admin_dashboard'))

    # For GET requests, return the form HTML to load into the modal
    return render_template('modal_form.html', form=form, model=model, record=record)


@bp.route('/edit/<model>/<int:record_id>', methods=['GET'])
@login_required
@admin_required
def edit_record_modal(model, record_id):
    # Query the correct record based on the model
    if model == 'inventory':
        record = Inventory.query.get(record_id)
        form = InventoryForm(obj=record)
    elif model == 'flock':
        record = Flock.query.get(record_id)
        form = FlockForm(obj=record)
    elif model == 'production':
        record = Production.query.get(record_id)
        form = ProductionForm(obj=record)
    elif model == 'health_record':
        record = HealthRecord.query.get(record_id)
        form = HealthRecordForm(obj=record)

    # Render the modal form template for the record
    return render_template('modal_form.html', form=form, model=model, record=record)


@bp.route('/delete-record/<model>/<int:record_id>')
@login_required
@admin_required
def delete_record(model, record_id):
    """
    Admin deletes a specific record based on the model.
    """
    if model == 'inventory':
        record = Inventory.query.get(record_id)
    elif model == 'production':
        record = Production.query.get(record_id)
    elif model == 'flock':
        record = Flock.query.get(record_id)
    elif model == 'health_record':
        record = HealthRecord.query.get(record_id)
    else:
        flash("Invalid model.", 'danger')
        return redirect(url_for('main.admin_dashboard'))

    if record:
        db.session.delete(record)
        db.session.commit()
        flash(f'{model} record has been deleted.', 'success')
    else:
        flash('Record not found.', 'danger')

    return redirect(url_for('main.admin_dashboard'))


@bp.route('/generate-report/<string:period>')
@login_required
@admin_required
def generate_report(period):
    """
    Generate weekly or monthly reports.
    """
    today = datetime.today()
    if period == 'weekly':
        start_date = today - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = today - timedelta(weeks=4)
    else:
        flash("Invalid report period", 'danger')
        return redirect(url_for('main.admin_dashboard'))

    # Filter data by date range
    inventories = Inventory.query.filter(Inventory.purchase_date >= start_date).all()
    productions = Production.query.filter(Production.date_collected >= start_date).all()
    flocks = Flock.query.filter(Flock.arrival_date >= start_date).all()
    health_records = HealthRecord.query.filter(HealthRecord.date_reported >= start_date).all()

    # Summarize flock data
    flock_summary = {
        'total_birds': sum([flock.quantity for flock in flocks]),
        'breeds': {flock.breed: sum([f.quantity for f in flocks if f.breed == flock.breed]) for flock in flocks},
        'birds_sold': sum([flock.sold for flock in flocks]),
        'birds_died': sum([flock.died for flock in flocks])
    }

    return render_template(
        'report.html',
        period=period,
        inventories=inventories,
        productions=productions,
        flock_summary=flock_summary,
        health_records=health_records
    )


@bp.route('/view-inventory')
@login_required
@admin_required
def view_inventory():
    """
    View all inventory records with the worker who entered each record.
    """
    inventories = Inventory.query.all()
    return render_template('view_inventory.html', inventories=inventories)


@bp.route('/view-flock')
@login_required
@admin_required
def view_flock():
    """
    View all inventory records with the worker who entered each record.
    """
    flocks = db.session.query(Flock, User).join(User).all()
    return render_template('view_flock.html', flocks=flocks)


@bp.route('/view-production')
@login_required
@admin_required
def view_production():
    """
    View all inventory records with the worker who entered each record.
    """
    # Query all production records along with the associated worker who added them
    productions = db.session.query(Production, User).join(User).all()
    return render_template('view_production.html', productions=productions)


@bp.route('/view-health_record')
@login_required
@admin_required
def view_health_record():
    """
    View all inventory records with the worker who entered each record.
    """
    health_records = HealthRecord.query.all()
    return render_template('view_health_records.html', health_records=health_records)
