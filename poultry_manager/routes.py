from flask import render_template, url_for, Blueprint, redirect, flash, jsonify
from flask_login import logout_user, login_user, login_required, current_user
from poultry_manager.forms import (RegisterForm, LoginForm, InventoryForm, ProductionForm, FlockForm, HealthRecordForm,
                                   AccountSettingsForm)
from poultry_manager import db
from poultry_manager.models.user import User, RoleEnum
from poultry_manager.middleware.access_control import admin_required, worker_required, admin_or_worker_required
from poultry_manager.models.inventory import Inventory
from poultry_manager.models.production import Production
from poultry_manager.models.flock import Flock
from poultry_manager.models.health_record import HealthRecord


bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/home')
def home_page():
    """
        Render the home page. Redirect authenticated users to their respective dashboards.
    """
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        elif current_user.is_worker():
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
            flash('Login failed. Check your username and password.', category='danger')

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


@bp.route('/account-settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    form = AccountSettingsForm()

    if form.validate_on_submit():
        if form.new_password.data:
            current_user.set_password(form.new_password.data)

        current_user.username = form.username.data
        current_user.email = form.email_address.data
        db.session.commit()
        flash('Your account has been updated!', category='success')
        return redirect(url_for('main.account_settings'))

    # Pre-fill the form with the user's current data
    form.username.data = current_user.username
    form.email_address.data = current_user.email

    return render_template('account_settings.html', form=form)


@bp.route('/workers-dashboard')
@login_required
@worker_required
def worker_dashboard():
    """
    Workers dashboard showing worker-specific options like adding inventory, viewing reports, etc.
    """
    return render_template('workers_dashboard.html', username=current_user.username, role=current_user.role.value)


@bp.route('/add_inventory', methods=['GET', 'POST'])
@login_required
@admin_or_worker_required
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
            user_id=current_user.id,
            created_by_username=current_user.username
        )
        db.session.add(new_inventory)
        db.session.commit()
        flash('Inventory item added successfully', 'success')
        # Redirect based on user role
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.worker_dashboard'))
    return render_template('inventory.html', form=form)


@bp.route('/add-production', methods=['GET', 'POST'])
@login_required
@admin_or_worker_required
def add_production():
    form = ProductionForm()
    if form.validate_on_submit():
        production_record = Production(
            number_eggs_collected=form.number_eggs_collected.data,
            eggs_sold=form.eggs_sold.data,
            date_collected=form.date_collected.data,
            user_id=current_user.id,
            created_by_username=current_user.username
        )
        db.session.add(production_record)
        db.session.commit()
        flash('Production record added successfully', 'success')
        # Redirect based on user role
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.worker_dashboard'))
    return render_template('production.html', form=form)


@bp.route('/add-flock', methods=['GET', 'POST'])
@login_required
@admin_or_worker_required
def add_flock():
    form = FlockForm()
    if form.validate_on_submit():
        new_flock = Flock(
            breed=form.breed.data,
            quantity=form.quantity.data,
            age=form.age.data,
            deaths=form.deaths.data,
            sold=form.sold.data,
            entry_date=form.entry_date.data,
            user_id=current_user.id,
            created_by_username=current_user.username
        )
        db.session.add(new_flock)
        db.session.commit()
        flash('Flock record added successfully', 'success')
        # Redirect based on user role
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.worker_dashboard'))
    return render_template('flock.html', form=form)


@bp.route('/add-health-record', methods=['GET', 'POST'])
@login_required
@admin_or_worker_required
def add_health_record():
    form = HealthRecordForm()
    if form.validate_on_submit():
        health_record = HealthRecord(
            number_sick=form.number_sick.data,
            symptom=form.symptom.data,
            medication_given=form.medication_given.data,
            date_reported=form.date_reported.data,
            user_id=current_user.id,
            created_by_username=current_user.username
        )
        db.session.add(health_record)
        db.session.commit()
        flash('Health record added successfully', 'success')
        # Redirect based on user role
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
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


@bp.route('/manage_workers', methods=['GET'])
@admin_required
@login_required
def manage_workers():
    workers = User.query.all()  # Fetch all workers
    return render_template('manage_workers.html', workers=workers)


@bp.route('/promote/<int:user_id>')
@login_required
@admin_required
def promote_worker(user_id):
    """Admin promotes a worker to admin"""
    worker = User.query.get_or_404(user_id)
    if worker.is_admin():
        flash("User is already an admin.", "warning")
        return redirect(url_for('main.manage_workers'))

    worker.role = RoleEnum.ADMIN
    db.session.commit()
    flash(f"{worker.username} has been promoted to admin.", "success")
    return redirect(url_for('main.manage_workers'))


@bp.route('/demote/<int:user_id>')
@login_required
@admin_required
def demote_worker(user_id):
    worker = User.query.get_or_404(user_id)
    if worker.is_worker():
        flash("User is already a worker.", "warning")
        return redirect(url_for('main.manage_workers'))

    worker.role = RoleEnum.WORKER
    db.session.commit()
    flash(f"{worker.username} has been demoted to worker.", "success")
    return redirect(url_for('main.manage_workers'))


@bp.route('/remove-worker/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_worker(user_id):
    """
    Admin removes (deletes) a worker from the system.
    """
    worker = User.query.get_or_404(user_id)
    db.session.delete(worker)
    db.session.commit()
    flash(f"{worker.username} has been removed.", "success")
    return redirect(url_for('main.manage_workers'))


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


@bp.route('/api/production-data')
@login_required
@admin_required
def production_data():
    productions = Production.query.all()
    data = {
        "labels": [p.date_collected.strftime("%Y-%m-%d") for p in productions],
        "data": [p.number_eggs_collected for p in productions]
    }
    return jsonify(data)


@bp.route('/api/health-record-data')
@login_required
@admin_required
def health_record_data():
    records = HealthRecord.query.all()
    symptoms = {}
    for record in records:
        symptom = record.symptom
        symptoms[symptom] = symptoms.get(symptom, 0) + 1

    data = {
        "labels": list(symptoms.keys()),
        "data": list(symptoms.values())
    }
    return jsonify(data)


@bp.route('/api/flock-data')
@login_required
@admin_required
def flock_data():
    flocks = Flock.query.all()
    breeds = {}
    for flock in flocks:
        breed = flock.breed
        breeds[breed] = breeds.get(breed, 0) + flock.quantity

    data = {
        "labels": list(breeds.keys()),
        "data": list(breeds.values())
    }
    return jsonify(data)
