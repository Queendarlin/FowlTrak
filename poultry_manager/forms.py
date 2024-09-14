from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms import SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Optional
from poultry_manager.models.user import User


class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField('Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password:', validators=[Length(min=7), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class InventoryForm(FlaskForm):
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
    """Form for recording production data."""
    number_eggs_collected = IntegerField('Number of Eggs Collected',
                                         validators=[DataRequired(),
                                                     NumberRange(min=0, message="Must be a non-negative value")])
    eggs_sold = IntegerField('Number of Eggs Sold',
                             validators=[NumberRange(min=0,
                                                     message="Must be a non-negative value")], default=0)
    date_collected = DateField('Date Collected', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Record')


class FlockForm(FlaskForm):
    breed = StringField('Breed', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    age = IntegerField('Age (Days)', validators=[DataRequired(), NumberRange(min=0)])
    deaths = IntegerField('Number of Deaths', default=0, validators=[NumberRange(min=0)])
    sold = IntegerField('Number of Chickens Sold', default=0, validators=[NumberRange(min=0)])
    submit = SubmitField('Submit Record')


class HealthRecordForm(FlaskForm):
    number_sick = IntegerField('Number of Sick Birds',
                               validators=[NumberRange(min=0, message="Must be a non-negative value")])
    symptom = StringField('Symptoms', validators=[Length(max=200), DataRequired()])
    medication_given = StringField('Medication Given', validators=[Length(max=200), DataRequired()])
    date_reported = DateField('Date Reported', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Record')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username:', validators=[Length(min=4, max=30), Optional()])
    email_address = StringField('Email Address:', validators=[Email(), Optional()])
    password1 = PasswordField('New Password:', validators=[Length(min=7), Optional()])
    password2 = PasswordField('Confirm New Password:', validators=[EqualTo('password1'), Optional()])
    submit = SubmitField('Update Profile')

    def validate_username(self, username_to_check):
        if username_to_check.data:
            user = User.query.filter_by(username=username_to_check.data).first()
            if user:
                raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        if email_address_to_check.data:
            email_address = User.query.filter_by(email=email_address_to_check.data).first()
            if email_address:
                raise ValidationError('Email Address already exists! Please try a different email address')


class DeleteRecordForm(FlaskForm):
    submit = SubmitField('Delete Record')