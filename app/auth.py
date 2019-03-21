from flask import render_template, Blueprint

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/login')
def login():
    """Auth: Login Page"""
    return render_template('auth/login.jinja2')


@auth_blueprint.route('/auth/logout')
def logout():
    """Auth: Logout Page"""
    return render_template('auth/logout.jinja2')


@auth_blueprint.route('/auth/register')
def register():
    """Auth: Login Page"""
    return render_template('auth/register.jinja2')
