import os
from flask import render_template, Blueprint, redirect, url_for, current_app
from flask_user import current_user, login_required
from app.forms.forms import CreateRevisionForm
from app.models import Revision, Submission, User
from werkzeug.utils import secure_filename
import datetime


revisions_blueprint = Blueprint('revisions', __name__)


@login_required
@revisions_blueprint.route('/')
def index():
    """nothing here"""
    return redirect(url_for('submissions.index'))


@login_required
@revisions_blueprint.route('/create/<submission_id>', methods=['GET', 'POST'])
def create(submission_id):
    """Create revision page"""
    # TODO Only allow if none exist or feedback has been received
    form = CreateRevisionForm()
    if form.validate_on_submit():
        f = form.file.data
        fname = secure_filename(f.filename)
        fileext = fname.rsplit('.', 1)[1].lower()
        filename = current_user.last_name + '_' + current_user.first_name + '_revision_' + \
                   datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.' + fileext
        f.save(os.path.join(current_app.config['SUBMISSION_FOLDER'], filename))

        params = {'filename': filename, 'submission_id': submission_id}
        revision_id = Revision.create_revision(params=params)

        return redirect(url_for('revisions.view', revision_id=revision_id))

    return render_template('revisions/create.jinja2',
                           form=form,
                           submission_id=submission_id)


@login_required
@revisions_blueprint.route('/view/<revision_id>')
def view(revision_id):
    """Revision view page"""
    revision = Revision.get_revision_by_id(revision_id=revision_id)
    submission = Submission.get_submission_by_id(submission_id=revision.submission_id)
    user = User.get_user_by_id(user_id=submission.user_id)
    return render_template('revisions/view.jinja2',
                           revision=revision,
                           submission=submission,
                           user=user)

