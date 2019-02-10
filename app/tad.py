from flask import render_template, Blueprint

tad_blueprint = Blueprint('tad', __name__)


@tad_blueprint.route('/tad/new')
def new():
    """Create submission page"""
    return render_template('tad/edit.jinja2', new=True)


@tad_blueprint.route('/tad/edit')
def edit():
    """Edit submission page"""
    return render_template('tad/edit.jinja2', new=False)
