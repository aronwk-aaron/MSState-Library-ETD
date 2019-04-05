from flask import current_app, flash
from flask_user import UserManager
from flask_user.forms import unique_email_validator, password_validator
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField, SubmitField, validators, FormField, \
    SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional

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
        DataRequired('MSU E-Mail is Required'),
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Password is Required'),
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
        flash('Invalid email or password', 'error')
        return False


class CustomRegisterForm(FlaskForm):
    """Registration form"""
    next = HiddenField()
    reg_next = HiddenField()

    # Login Info
    email = StringField('MSU E-Mail', validators=[
        DataRequired(),
        validators.Email('Invalid email address'),
        unique_email_validator,
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        password_validator
    ])
    retype_password = PasswordField('Retype Password', validators=[
        validators.EqualTo('password', message='Passwords did not match')
    ])

    # MSU Info
    net_id = StringField('NetID', validators=[
        DataRequired()
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        DataRequired(),
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = DepartmentSelectField('Department', validators=[
        DataRequired()
    ])

    # Personal Info
    first_name = StringField('First name', validators=[
        DataRequired()
    ])
    middle_name = StringField('Middle name', validators=[
        DataRequired()
    ])
    last_name = StringField('Last name', validators=[
        DataRequired()
    ])
    birth_date = DateField('Date of Birth', format='%Y-%m-%d', validators=[
        DataRequired()
    ])
    pref_name = StringField('Prefered name (if different from first name)', validators=[
        Optional()
    ])
    maiden_name = StringField('Maiden name (if applicable)', validators=[
        Optional()
    ])

    # Contact Info

    sec_email = StringField('Personal email (Optional)', validators=[
        Optional(),
        validators.Email('Invalid email address'),
        unique_email_validator
    ])
    prim_phone = StringField('Primary phone', validators=[
        DataRequired(),
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (Optional)', validators=[
        Optional(),
        validate_phone
    ])
    # address = FormField(CompleteAddressForm)
    thoroughfare = StringField('Street address', validators=[
        DataRequired(),
    ])
    premise = StringField('Apt/Suite/Box number', validators=[
        Optional(),
    ])
    locality = StringField('City/Town', validators=[
        DataRequired(),
    ])
    administrative_area = StringField('State/Province/Region', validators=[
        DataRequired(),
        validate_subdivision
    ])
    postal_code = StringField('ZIP/Postal code', validators=[
        DataRequired(),
    ])
    country = CountrySelectField('Country', validators=[
        DataRequired(),
    ])
    invite_token = HiddenField('Token')

    submit = SubmitField('Register')


class CustomEditUserProfileForm(FlaskForm):
    """Edit Profile Form form"""
    # MSU Info
    net_id = StringField('NetID', validators=[
        DataRequired()
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        DataRequired(),
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = DepartmentSelectField('Department', validators=[
        DataRequired()
    ])

    # Personal Info
    first_name = StringField('First name', validators=[
        DataRequired()
    ])
    middle_name = StringField('Middle name', validators=[
        DataRequired()
    ])
    last_name = StringField('Last name', validators=[
        DataRequired()
    ])
    birth_date = DateField('Date of birth', format='%Y-%m-%d', validators=[
        DataRequired()
    ])
    pref_name = StringField('Prefered name (if different from first name)', validators=[
        Optional()
    ])
    maiden_name = StringField('Maiden name (if applicable)', validators=[
        Optional()
    ])

    # Contact Info

    sec_email = StringField('Personal email (Optional)', validators=[
        Optional(),
        validators.Email('Invalid email address'),
    ])
    prim_phone = StringField('Primary phone', validators=[
        DataRequired(),
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (Optional)', validators=[
        Optional(),
        validate_phone
    ])
    # address = FormField(CompleteAddressForm)

    thoroughfare = StringField('Street address', validators=[
        DataRequired(),
    ])
    premise = StringField('Apt/Suite/Box number', validators=[
        Optional(),
    ])
    locality = StringField('City/Town', validators=[
        DataRequired(),
    ])
    administrative_area = StringField('State/Province/Region', validators=[
        DataRequired(),
        validate_subdivision
    ])
    postal_code = StringField('ZIP/Postal code', validators=[
        DataRequired(),
    ])
    country = CountrySelectField('Country', validators=[
        DataRequired(),
    ])

    submit = SubmitField('Update')


class CreateSubmissionForm(FlaskForm):
    id = HiddenField()
    user_id = HiddenField()
    title = StringField('Title', validators=[
        DataRequired()
    ])
    abstract = TextAreaField('Abstract', validators=[
        DataRequired()
    ])

    type = SelectField('Document type', validators=[
        DataRequired()
    ], choices=[
        ('0', 'Master\'s Thesis'),
        ('1', 'Educational Specialist\'s Thesis'),
        ('2', 'Doctoral Disseration'),
    ])

    release = SelectField('Release type', validators=[
        DataRequired()
    ], choices=[
        ('0', 'Worldwide'),
        ('1', 'Restricted'),
        ('2', 'Embargo'),
    ])

    professor = StringField('Major Professor\'s NetID', validators=[
        Optional()
    ])

    years = SelectField('Restict time (if Restricted is selected)', validators=[
        DataRequired()
    ], choices=[
        ('0', ''),
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
    ])

    signature = FileField('Signature file', validators=[
        FileRequired(),
        FileAllowed(['pdf'], "PDF's only!")
    ])

    submit = SubmitField('Create Submission')
