import os
from flask import render_template, Blueprint, redirect, url_for, current_app
from flask_user import current_user, login_required
from app.forms.forms import CreateSubmissionForm
from app.models import Submission, User, Revision
from werkzeug.utils import secure_filename


submissions_blueprint = Blueprint('submissions', __name__)


@submissions_blueprint.route('/')
@login_required
def index():
    """Catalog of Submissions"""

    result = Submission.query \
        .join(User, User.id == Submission.user_id) \
        .add_columns(User.id, User.first_name, User.last_name, Submission.id, Submission.title, Submission.started) \
        .filter(User.id == Submission.user_id) \
        .filter(Submission.user_id == User.id)

    return render_template('submissions/index.jinja2', submissions=result)


@submissions_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create submission page"""

    form = CreateSubmissionForm()
    if form.validate_on_submit():
        f = form.signature.data
        fname = secure_filename(f.filename)
        fileext = fname.rsplit('.', 1)[1].lower()
        filename = current_user.last_name + '_' + current_user.first_name + '_' + form.title.data + '_signatures.' + fileext
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
    user = User.get_user_by_id(user_id=submission.user_id)
    return render_template('submissions/view.jinja2',
                           submission=submission,
                           revisions=revisions,
                           user=user)




