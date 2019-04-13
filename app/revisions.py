import os
from flask import render_template, Blueprint, redirect, url_for, current_app
from flask_user import current_user, login_required, roles_required
from app.forms.forms import CreateRevisionForm, CreateReviewForm
from app.models import Revision, Submission, User, Review
from werkzeug.utils import secure_filename
import datetime

revisions_blueprint = Blueprint('revisions', __name__)


@revisions_blueprint.route('/')
@login_required
def index():
    """nothing here"""
    return redirect(url_for('submissions.index'))


@revisions_blueprint.route('/create/<submission_id>', methods=['GET', 'POST'])
@login_required
@roles_required('user')
def create(submission_id):
    """Create revision page"""
    # TODO make this nicer....
    form = CreateRevisionForm()
    submission = Submission.get_submission_by_id(submission_id=submission_id)
    # if current user does not own submission
    # or if submission has been approved, they can't create revision
    if submission.user_id != current_user.id or submission.state:
        return redirect(url_for('submissions.view', submission_id=submission_id))
    else:
        revisions = Revision.get_all_revisions_by_submission_id(submission_id=submission_id)
        # if a revision exist
        if revisions:
            # if latest revision has not been reviewed
            if Review.get_review_by_revision_id(revision_id=revisions[-1].id) is None:
                return redirect(url_for('revisions.view', revision_id=revisions[-1].id))
            # else latest revision has been reviewed
            else:
                # if a post process it
                if form.validate_on_submit():
                    revision_id = create_post(form, submission_id)
                    return redirect(url_for('revisions.view', revision_id=revision_id))
                # else present the create page
                else:
                    return render_template('revisions/create.jinja2',
                                           form=form,
                                           submission_id=submission_id)
        # if no revision exists
        else:
            # if a post process it
            if form.validate_on_submit():
                revision_id = create_post(form, submission_id)
                return redirect(url_for('revisions.view', revision_id=revision_id))
            # else present the create page
            else:
                return render_template('revisions/create.jinja2',
                                       form=form,
                                       submission_id=submission_id)


def create_post(form, submission_id):
    f = form.file.data
    fname = secure_filename(f.filename)
    fileext = fname.rsplit('.', 1)[1].lower()
    filename = '{last_name}_{first_name}_revision_{time}.{ext}'.format(
        last_name=current_user.last_name,
        first_name=current_user.first_name,
        time=datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
        ext=fileext)

    f.save(os.path.join(current_app.config['SUBMISSION_FOLDER'], filename))

    params = {'filename': filename, 'submission_id': submission_id}
    revision_id = Revision.create_revision(params=params)

    return revision_id


@revisions_blueprint.route('/view/<revision_id>')
@login_required
def view(revision_id):
    """Revision view page"""
    revision = Revision.get_revision_by_id(revision_id=revision_id)
    submission = Submission.get_submission_by_id(submission_id=revision.submission_id)
    # if elevated user or submission owner or major professor
    if current_user.has_roles(['admin', 'viewer', 'reviewer', 'helper']) or \
       current_user.id == submission.user_id or \
       current_user.net_id == submission.professor:
        review_data = Review.get_review_by_revision_id(revision_id=revision_id)
        user = User.get_user_by_id(user_id=submission.user_id)
        return render_template('revisions/view.jinja2',
                               revision=revision,
                               submission=submission,
                               user=user,
                               review=review_data)
    # else not supposed to view it
    else:
        return redirect(url_for('submissions.index'))


@revisions_blueprint.route('/review/<revision_id>', methods=['GET', 'POST'])
@login_required
@roles_required('reviewer')
def review(revision_id):
    """Revision review page"""
    # only allow if reviewer
    form = CreateReviewForm()
    revision = Revision.get_revision_by_id(revision_id=revision_id)
    submission = Submission.get_submission_by_id(submission_id=revision.submission_id)

    # if has been approved
    if submission.state:
        return redirect(url_for('revisions.view', revision_id=revision_id))

    # if post
    if form.validate_on_submit():
        # if approved
        if form.approve.data:
            Submission.complete_submission_by_id(submission_id=revision.submission_id)
            return redirect(url_for('submissions.view', submission_id=revision.submission_id))
        else:
            params = {'form_data': form.data, 'revision_id': revision_id, 'reviewer_id': current_user.id}
            Review.create_review(params=params)
            return redirect(url_for('revisions.view', revision_id=revision_id))
    else:
        user = User.get_user_by_id(user_id=submission.user_id)
        return render_template('revisions/review.jinja2',
                               revision=revision,
                               submission=submission,
                               user=user,
                               form=form)
