from flask import render_template, Blueprint

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def splash():
    """Splash Page"""
    return render_template('main/splash.jinja2')


@main_blueprint.route('/home')
def index():
    """Home/Index Page"""
    return render_template('main/index.jinja2')


@main_blueprint.route('/dashboard')
def dashboard():
    """Dashboard Page"""
    return render_template('main/dashboard.jinja2')


@main_blueprint.route('/profile')
def profile():
    """Profile Page"""
    return render_template('main/profile.jinja2')


@main_blueprint.route('/signed-out')
def signed_out():
    """Sign out landing page"""
    return render_template('main/signed_out.jinja2')
