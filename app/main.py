from flask import render_template, Blueprint, url_for, redirect, send_from_directory
from flask_user import current_user, login_required, current_app
from app.models import Submission, Revision

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
@login_required
def index():
    """Home/Index Page"""
    return render_template('main/index.jinja2')


@main_blueprint.route('/profile')
@login_required
def profile():
    """Profile Page"""
    # do not need to pass data, since we can just access the current_user method in the template
    return render_template('main/profile.jinja2')


@main_blueprint.route('/uploads/signatures/<filename>')
@login_required
def uploads_signatures(filename):
    query = Submission.get_submission_by_signature(signature_filename=filename)
    # if elevated user or submission owner or major professor
    if current_user.has_roles(['admin', 'viewer', 'reviewer', 'helper']) or \
        current_user.id == query.user_id or \
        current_user.net_id == query.professor:
        return send_from_directory(current_app.config['SIGNATURE_FOLDER'], query.signature_file)
    else:
        return redirect(url_for('main.index'))


@main_blueprint.route('/uploads/submissions/<filename>')
@login_required
def uploads_submissions(filename):
    query = Revision.get_revision_by_filename(filename=filename)
    submission = Submission.get_submission_by_id(submission_id=query.submission_id)
    # if elevated user or submission owner or major professor
    if current_user.has_roles(['admin', 'viewer', 'reviewer', 'helper']) or \
        current_user.id == submission.user_id or \
        current_user.net_id == submission.professor:
        return send_from_directory(current_app.config['SUBMISSION_FOLDER'], query.file)
    else:
        return redirect(url_for('main.index'))


@main_blueprint.route('/documents/<filename>')
@login_required
def serve_documents(filename):
    return send_from_directory(current_app.config['DOCUMENT_FOLDER'], filename)


@main_blueprint.route('/user/signed-out')
def signed_out():
    """Sign out landing page"""
    return render_template('flask_user/signed_out.html')


@main_blueprint.route('/about')
@login_required
def about():
    """About Page"""
    return render_template('main/about.jinja2')
