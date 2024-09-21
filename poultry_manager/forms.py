"""
This module defines forms for the FowlTrak application, handling user registration,
login, account settings, inventory management, production data entry, flock management,
and health record tracking. These forms use Flask-WTF and WTForms to manage form validation.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms import SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Optional
from poultry_manager.models.user import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    """
        Form for user registration, allowing users to create an account with a username, email,
        and password. Includes validation for unique usernames and email addresses.

        Methods:
            validate_username: Ensures the username is unique.
            validate_email_address: Ensures the email address is unique.
    """
    username = StringField('Username:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField('Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password:', validators=[Length(min=7), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')

    def validate_username(self, username_to_check):
        """
            Validates that the username is unique and not already taken.

           :param username_to_check: The username to check.
           :raises ValidationError: If the username already exists.
        """
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        """
            Validates that the email address is unique and not already in use.

            :param email_address_to_check: The email address to check.
            :raises ValidationError: If the email address already exists.
        """
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')


class LoginForm(FlaskForm):
    """
        Form for user login, accepting a username and password.
    """
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class AccountSettingsForm(FlaskForm):
    """
        Form for updating account settings, including changing username, email address,
        and password. Includes validation for the current password and unique username and email.

        Methods:
            validate_username: Ensures that the new username is unique.
            validate_email_address: Ensures that the new email address is unique.
            validate_current_password: Ensures the current password is correct before making updates.
    """
    username = StringField('Username:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField('Email Address:', validators=[Email(), DataRequired()])
    current_password = PasswordField('Current Password:', validators=[DataRequired()])
    new_password = PasswordField('New Password:', validators=[Length(min=7), Optional()])
    confirm_new_password = PasswordField('Confirm New Password:', validators=[EqualTo('new_password'), Optional()])
    submit = SubmitField('Update Account')

    def validate_username(self, username_to_check):
        """
            Validates that the new username is unique if it's different from the current username.

            :param username_to_check: The new username to check.
            :raises ValidationError: If the username already exists.
        """
        if username_to_check.data != current_user.username:
            user = User.query.filter_by(username=username_to_check.data).first()
            if user:
                raise ValidationError('Username already exists! Please try a different username.')

    def validate_email_address(self, email_address_to_check):
        """
            Validates that the new email address is unique if it's different from the current email.

            :param email_address_to_check: The new email address to check.
            :raises ValidationError: If the email address already exists.
        """
        if email_address_to_check.data != current_user.email:
            email_address = User.query.filter_by(email=email_address_to_check.data).first()
            if email_address:
                raise ValidationError('Email Address already exists! Please try a different email address.')

    def validate_current_password(self, current_password):
        """
            Validates the current password to ensure it's correct before allowing account changes.

            :param current_password: The current password input.
            :raises ValidationError: If the current password is incorrect.
        """
        if not current_user.check_password(current_password.data):
            raise ValidationError('Current password is incorrect.')


class InventoryForm(FlaskForm):
    """
        Form for recording inventory data including item name, category, quantity, unit, cost, and purchase details.
    """
    item_name = StringField('Item Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Livestock', 'Livestock'),
                                                ('Supplies', 'Supplies'), ('Equipment', 'Equipment'),
                                                ('Utilities', 'Utilities')], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    unit = StringField('Unit (e.g., kg, liters, bags, pc)', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    currency = SelectField('Currency', choices=[('USD', 'USD'), ('EUR', 'EUR'),
                                                ('NGN', 'NGN')], validators=[DataRequired()])
    purchase_order_number = StringField('Purchase Order Number', validators=[Optional()])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Record')


class ProductionForm(FlaskForm):
    """
    Form for recording egg production data, including the number of eggs collected, sold, and the date of collection.
    """
    number_eggs_collected = IntegerField('Number of Eggs Collected',
                                         validators=[DataRequired(),
                                                     NumberRange(min=0, message="Must be a non-negative value")])
    eggs_sold = IntegerField('Number of Eggs Sold',
                             validators=[NumberRange(min=0,
                                                     message="Must be a non-negative value")], default=0)
    date_collected = DateField('Date Collected', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Record')


class FlockForm(FlaskForm):
    """
        Form for managing flock data, including breed, quantity, age, deaths, sales, and entry date.
    """
    breed = StringField('Breed', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    age = IntegerField('Age (Days)', validators=[DataRequired(), NumberRange(min=0)])
    deaths = IntegerField('Number of Deaths', default=0, validators=[NumberRange(min=0)])
    sold = IntegerField('Number of Chickens Sold', default=0, validators=[NumberRange(min=0)])
    entry_date = DateField('Date Entered', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Record')


class HealthRecordForm(FlaskForm):
    """
        Form for tracking bird health records, including sick birds, symptoms, medication, and date reported.
    """
    number_sick = IntegerField('Number of Sick Birds',
                               validators=[NumberRange(min=0, message="Must be a non-negative value")])
    symptom = StringField('Symptoms', validators=[Length(max=200), DataRequired()])
    medication_given = StringField('Medication Given', validators=[Length(max=200), DataRequired()])
    date_reported = DateField('Date Reported', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Record')
