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
