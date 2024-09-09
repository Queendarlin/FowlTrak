from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
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

