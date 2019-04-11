import os
from flask import render_template, Blueprint, redirect, url_for, current_app
from flask_user import current_user, login_required, roles_required
from app.forms.forms import CreateSubmissionForm
from app.models import Submission, User, Revision, Review
from werkzeug.utils import secure_filename

submissions_blueprint = Blueprint('submissions', __name__)


@submissions_blueprint.route('/')
@login_required
def index():
    """Catalog of Submissions"""

    if current_user.has_roles(['admin', 'viewer', 'reviewer', 'helper']):
        results = Submission.get_all()
    else:
        results = Submission.get_all_submissions_by_user_id(user_id=current_user.id)

    return render_template('submissions/index.jinja2', submissions=results)


@submissions_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@roles_required('user')
def create():
    """Create submission page"""

    form = CreateSubmissionForm()
    if form.validate_on_submit():
        f = form.signature.data
        fname = secure_filename(f.filename)
        fileext = fname.rsplit('.', 1)[1].lower()
        filename = '{last_name}_{first_name}_{title}_signatures.{ext}'.format(
            last_name=current_user.last_name,
            first_name=current_user.first_name,
            title=form.title.data,
            ext=fileext)
        f.save(os.path.join(current_app.config['SIGNATURE_FOLDER'], filename))

        form.user_id.data = current_user.id
        params = {'form_data': form.data, 'filename': filename}
        submission_id = Submission.create_submission(params=params)

        return redirect(url_for('revisions.create', submission_id=submission_id))

    return render_template('submissions/create.jinja2', form=form)


@submissions_blueprint.route('/view/<submission_id>')
@login_required
def view(submission_id):
    """Submission revision view page"""
    submission = Submission.get_submission_by_id(submission_id=submission_id)
    revisions = Revision.get_all_revisions_by_submission_id(submission_id=submission_id)
    review_last = False
    if revisions:
        # if latest revision has not been reviewed
        if Review.get_review_by_revision_id(revision_id=revisions[-1].id):
            review_last = True
    user = User.get_user_by_id(user_id=submission.user_id)

    # if elevated user or submission owner or major professor
    if current_user.has_roles(['admin', 'viewer', 'reviewer', 'helper']) or \
        current_user.id == submission.user_id or \
        current_user.net_id == submission.professor:
        return render_template('submissions/view.jinja2',
                               submission=submission,
                               revisions=revisions,
                               user=user,
                               review_last=review_last)
    # else not supposed to view it
    else:
        return redirect(url_for('submissions.index'))
