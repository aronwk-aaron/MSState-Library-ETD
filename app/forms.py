from flask import current_app, flash
from flask_user import UserManager
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from app import models


class CustomUserManager(UserManager):

    # noinspection PyAttributeOutsideInit
    def customize(self, app):
        self.LoginFormClass = CustomLoginForm


class CustomLoginForm(FlaskForm):
    """Login form"""
    next = HiddenField()
    reg_next = HiddenField()

    netid = StringField('NetID', validators=[
        DataRequired('NetID is required'),
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Password is required'),
    ])
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Sign in')

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

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
