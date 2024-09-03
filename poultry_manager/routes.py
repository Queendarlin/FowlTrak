from flask import render_template, url_for, Blueprint, redirect

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/home')
def home_page():
    return render_template('home.html')


@bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@bp.route('/inventory')
def inventory_page():
    return render_template('inventory.html')


@bp.route('/health-report')
def health_page():
    return render_template('health.html')


@bp.route('/production-reports')
def production_page():
    return render_template('production.html')


@bp.route('/user-management')
def user_page():
    return render_template('user.html')


@bp.route('/register-account', methods=['GET', 'POST'])
def register_page():
    return render_template('register.html')


@bp.route('/login-user', methods=['GET, POST'])
def login_page():
    return render_template('login.html')


@bp.route('/logout')
def logout_page():
    if True:
        return redirect(url_for('dashboard_page'))
    return render_template('login.html')


@bp.route('/account-settings', methods=['GET', 'POST'])
def account_settings():
    return render_template('account_settings.html')


@bp.route('/update_account', methods=['POST'])
def update_account():
    return url_for('account_settings')
