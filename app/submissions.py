import os
from flask import render_template, Blueprint, redirect, url_for, request, current_app, send_from_directory
from flask_user import current_user, login_required
from app.forms.forms import CreateSubmissionForm
from app.models import Submission, User
from werkzeug.utils import secure_filename


submissions_blueprint = Blueprint('submissions', __name__)


@login_required
@submissions_blueprint.route('/')
@submissions_blueprint.route('/catalog')
def index():
    """Catalog of TADs"""

    result = Submission.query \
        .join(User, User.id == Submission.user_id) \
        .add_columns(User.id, User.first_name, User.last_name, Submission.id, Submission.title, Submission.started) \
        .filter(User.id == Submission.user_id) \
        .filter(Submission.user_id == User.id) \
        .filter(User.id == current_user.id)

    return render_template('submission/index.jinja2', tads=result)


@login_required
@submissions_blueprint.route('/new', methods=['GET', 'POST'])
def new():
    """Create submission page"""

    form = CreateSubmissionForm()
    if form.validate_on_submit():
        f = form.signature.data
        fname = secure_filename(f.filename)
        fileext = fname.rsplit('.', 1)[1].lower()
        filename = 'signatures/' + current_user.last_name + '_' + current_user.first_name + '_' + form.title.data + '_signatures.' + fileext
        f.save(os.path.join(current_app.instance_path, filename))
        return redirect(url_for('main.uploads', filename=filename))

    return render_template('submission/create_submission.jinja2',
                           new=True,
                           form=form)


@login_required
@submissions_blueprint.route('/<tad_id>/edit', methods=['GET', 'POST'])
def edit(tad_id):
    """Edit submission page"""
    return render_template('submission/create_submission.jinja2',
                           new=False,
                           tad_id=tad_id,
                           form=CreateSubmissionForm())


@login_required
@submissions_blueprint.route('/rev/<rev_id>')
def revision(tad_id, rev_id):
    """TAD revision view page"""
    return render_template('submission/revision.jinja2',
                           tad_id=tad_id,
                           rev_id=rev_id)


@login_required
@submissions_blueprint.route('/<tad_id>')
def view(tad_id):
    """TAD revision view page"""
    return render_template('submission/view.jinja2',
                           tad_id=tad_id)


@login_required
@submissions_blueprint.route('/portfolio')
def portfolio():
    """User's TAD portfolio page"""
    return render_template('submission/portfolio.jinja2')


