from flask import render_template, Blueprint, redirect, url_for

from app.forms.forms import CreateSubmissionForm
from app.models import Submission, User

tad_blueprint = Blueprint('tad', __name__)


@tad_blueprint.route('/tad/new', methods=['GET', 'POST'])
def new():
    """Create submission page"""

    form = CreateSubmissionForm()
    if form.validate_on_submit():

        return redirect(url_for('tad.edit', form.id))

    return render_template('tad/edit.jinja2',
                           new=True,
                           form=CreateSubmissionForm())


@tad_blueprint.route('/tad/<tad_id>/edit', methods=['GET', 'POST'])
def edit(tad_id):
    """Edit submission page"""
    return render_template('tad/edit.jinja2',
                           new=False,
                           tad_id=tad_id,
                           form=CreateSubmissionForm())


@tad_blueprint.route('/tad/<tad_id>/rev/<rev_id>')
def revision(tad_id, rev_id):
    """TAD revision view page"""
    return render_template('tad/revision.jinja2',
                           tad_id=tad_id,
                           rev_id=rev_id)


@tad_blueprint.route('/tad/<tad_id>')
def view(tad_id):
    """TAD revision view page"""
    return render_template('tad/view.jinja2',
                           tad_id=tad_id)


@tad_blueprint.route('/tad/portfolio')
def portfolio():
    """User's TAD portfolio page"""
    return render_template('tad/portfolio.jinja2')


@tad_blueprint.route('/tad/')
@tad_blueprint.route('/tad/catalog')
def catalog():
    """Catalog of TADs"""

    tads = Submission.query \
        .join(User, User.id == Submission.user_id) \
        .add_columns(User.id, User.first_name, User.last_name, Submission.id, Submission.title, Submission.started) \
        .filter(User.id == Submission.user_id) \
        .filter(Submission.user_id == User.id)

    return render_template('tad/catalog.jinja2', tads=tads)
