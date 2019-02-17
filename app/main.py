from flask import render_template, Blueprint

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    """Home/Index Page

    """
    return render_template('main/index.jinja2')


@main_blueprint.route('/login')
def splash():
    """Login Page
    Login with CAS
    """
    return render_template('main/login.jinja2')


@main_blueprint.route('/dashboard')
def dashboard():
    """Dashboard Page"""
    return render_template('main/dashboard.jinja2')


@main_blueprint.route('/profile/<id>')
def profile(id):
    """Profile Page
    View Profile
    """
    return render_template('main/profile.jinja2')


@main_blueprint.route('/profile/<id>/edit')
def profile_edit(id):
    """Profile Edit Page
    Edit Profile
    """
    return render_template('main/profile_edit.jinja2', id=id)


