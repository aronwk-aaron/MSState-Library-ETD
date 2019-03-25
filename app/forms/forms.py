from flask import current_app, flash
from flask_user import UserManager
from flask_user.forms import unique_email_validator, password_validator
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField, SubmitField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import required, optional

from app import models
from app.forms.fields import DepartmentSelectField, CountrySelectField
from app.forms.validators import validate_phone, validate_subdivision


class CustomUserManager(UserManager):

    # noinspection PyAttributeOutsideInit
    def customize(self, app):
        self.LoginFormClass = CustomLoginForm
        self.RegisterFormClass = CustomRegisterForm
        self.EditUserProfileFormClass = CustomEditUserProfileForm


class CustomLoginForm(FlaskForm):
    """Login form"""
    next = HiddenField()
    reg_next = HiddenField()

    email = StringField('MSU E-Mail', validators=[
        required('MSU E-Mail is required'),
    ])
    password = PasswordField('Password', validators=[
        required('Password is required'),
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

        # find user by email
        user = user_manager.db_manager.db_adapter.ifind_first_object(models.User, email=self.email.data)

        # handle successful authentication
        if user and user_manager.verify_password(self.password.data, user.password):
            return True

        # unsuccessful authentication
        flash('Invalid E-Mail or Password', 'error')
        return False


class CustomRegisterForm(FlaskForm):
    """Registration form"""
    next = HiddenField()
    reg_next = HiddenField()

    # Login Info
    email = StringField('MSU E-Mail', validators=[
        required,
        validators.Email('Invalid email address'),
        unique_email_validator,
    ])
    password = PasswordField('Password', validators=[
        required,
        password_validator
    ])
    retype_password = PasswordField('Retype Password', validators=[
        validators.EqualTo('password', message='Passwords did not match')
    ])

    # MSU Info
    net_id = StringField('NetID', validators=[
        required
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        required,
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = DepartmentSelectField('Department', validators=[
        required
    ])

    # Personal Info
    first_name = StringField('First name', validators=[
        required
    ])
    middle_name = StringField('Middle name', validators=[
        required
    ])
    last_name = StringField('Last name', validators=[
        required
    ])
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[
        required
    ])
    pref_name = StringField('Prefered name (If different from first name)', validators=[
        optional
    ])
    maiden_name = StringField('Maiden name (If Applicable)', validators=[
        optional
    ])

    # Contact Info

    sec_email = StringField('Personal E-Mail (optional)', validators=[
        optional,
        validators.Email('Invalid email address'),
        unique_email_validator
    ])
    prim_phone = StringField('Primary phone', validators=[
        required,
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (optional)', validators=[
        optional,
        validate_phone
    ])
    country = CountrySelectField('Country', validators=[
        required,
    ])
    administrative_area = StringField('State / Province / Region', validators=[
        required,
        validate_subdivision
    ])
    locality = StringField('City / Town', validators=[
        required,
    ])
    postal_code = StringField('Postal code / ZIP Code', validators=[
        required,
    ])
    thoroughfare = StringField('Street address', validators=[
        required,
    ])
    premise = StringField('Apartment, Suite, Box number, etc.', validators=[
        optional,
    ])

    invite_token = HiddenField('Token')

    submit = SubmitField('Register')


class CustomEditUserProfileForm(FlaskForm):
    """Edit Profile Form form"""
    # MSU Info
    net_id = StringField('NetID', validators=[
        required
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        required,
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = DepartmentSelectField('Department', validators=[
        required
    ])

    # Personal Info
    first_name = StringField('First name', validators=[
        required
    ])
    middle_name = StringField('Middle name', validators=[
        required
    ])
    last_name = StringField('Last name', validators=[
        required
    ])
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[
        required
    ])
    pref_name = StringField('Prefered name (If different from first name)', validators=[
        optional
    ])
    maiden_name = StringField('Maiden name (If Applicable)', validators=[
        optional
    ])

    # Contact Info

    sec_email = StringField('Personal E-Mail (optional)', validators=[
        optional,
        validators.Email('Invalid email address'),
    ])
    prim_phone = StringField('Primary phone', validators=[
        required,
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (optional)', validators=[
        optional,
        validate_phone
    ])
    country = CountrySelectField('Country', validators=[
        required,
    ])
    administrative_area = StringField('State / Province / Region', validators=[
        required,
        validate_subdivision
    ])
    locality = StringField('City / Town', validators=[
        required,
    ])
    postal_code = StringField('Postal code / ZIP Code', validators=[
        required,
    ])
    thoroughfare = StringField('Street address', validators=[
        required,
    ])
    premise = StringField('Apartment, Suite, Box number, etc.', validators=[
        optional,
    ])

    submit = SubmitField('Update')
