from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

from app.models import User, db

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    """Auth: Login Page"""
    if request.method == 'GET':
        return render_template('auth/login.jinja2')

    db.create_all()
    netid = request.form['netid']
    password = request.form['password']

    registered_user = User.query.filter_by(netid=netid).first()

    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('auth.login'))

    if check_password_hash(password, registered_user.password):
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('auth.login'))

    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@auth_blueprint.route('/auth/logout')
def logout():
    """Auth: Logout Page"""
    return render_template('auth/logout.jinja2')


@auth_blueprint.route('/auth/register')
def register():
    """Auth: Login Page"""
    return render_template('auth/register.jinja2')
