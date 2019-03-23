import phonenumbers as phonenumbers
from flask import current_app, flash
from flask_user import UserManager
from flask_user.forms import unique_email_validator, password_validator
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField, SubmitField, validators, ValidationError
from wtforms.fields.html5 import DateField

from app import models


# noinspection PyBroadException,PyUnusedLocal
def validate_phone(form, field):
    """Validates a field for a valid phone number

    Args:
        form: REQUIRED, the field's parent form
        field: REQUIRED, the field with data

    Returns:
        None, raises ValidationError if failed
    """
    if len(field.data) > 16:
        raise ValidationError('Invalid phone number')
    try:
        input_number = phonenumbers.parse(field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError('Invalid phone number')
    except Exception:
        input_number = phonenumbers.parse("+1" + field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError('Invalid phone number')


class CustomUserManager(UserManager):

    # noinspection PyAttributeOutsideInit
    def customize(self, app):
        self.LoginFormClass = CustomLoginForm
        self.RegisterFormClass = CustomRegisterForm


class CustomLoginForm(FlaskForm):
    """Login form"""
    next = HiddenField()
    reg_next = HiddenField()

    netid = StringField('NetID', validators=[
        validators.DataRequired('NetID is required'),
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired('Password is required'),
    ])
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Sign in')

    def __init_(self, *args, **kwargs):
        super(CustomLoginForm, self).__init_(*args, **kwargs)

    def validate(self):
        # grab the user manager
        user_manager = current_app.user_manager

        # handle invalid fields
        if not super(CustomLoginForm, self).validate():
            return False

        # find user by netid
        user = user_manager.db_manager.db_adapter.ifind_first_object(models.User, netid=self.netid.data)

        # handle successful authentication
        if user and user_manager.verify_password(self.password.data, user.password):
            return True

        # unsuccessful authentication
        flash('Invalid NetID or Password', 'error')
        return False


class CustomRegisterForm(FlaskForm):
    """Registration form"""
    next = HiddenField()
    reg_next = HiddenField()

    # Personal Info
    first_name = StringField('First name', validators=[
        validators.DataRequired()
    ])
    middle_name = StringField('Middle name', validators=[
        validators.DataRequired()
    ])
    last_name = StringField('Last name', validators=[
        validators.DataRequired()
    ])
    birth_date = DateField('Birth date', format='%m-%d-%Y', validators=[
        validators.DataRequired()
    ])

    # MSU Info
    netid = StringField('NetID', validators=[
        validators.DataRequired()
    ])
    msuid = StringField('MSU ID (9-digit WITH dashes)', validators=[
        validators.DataRequired(),
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = StringField('Department', validators=[
        validators.DataRequired()
    ])

    # Contact Info
    email = StringField('Primary email', validators=[
        validators.DataRequired(),
        validators.Email('Invalid email address'),
        unique_email_validator
    ])
    sec_email = StringField('Secondary email', validators=[
        validators.Optional(),
        validators.Email('Invalid email address'),
        unique_email_validator
    ])
    prim_phone = StringField('Primary phone', validators=[
        validators.DataRequired(),
        validate_phone
    ])
    sec_phone = StringField('Secondary phone', validators=[
        validators.Optional(),
        validate_phone
    ])

    # Login Info
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        password_validator
    ])
    retype_password = PasswordField('Retype Password', validators=[
        validators.EqualTo('password', message='Passwords did not match')
    ])

    invite_token = HiddenField('Token')

    submit = SubmitField('Register')
