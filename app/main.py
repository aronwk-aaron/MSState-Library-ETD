import os
from flask import render_template, Blueprint, url_for, redirect, send_from_directory, request
from flask_user import current_user, login_required, current_app, roles_required
from app.models import Submission, Revision, Document, User, UsersRoles
from app.forms.forms import CreateDocumentForm, UpdateRoleForm
from werkzeug.utils import secure_filename
import datetime

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
    return send_from_directory(current_app.config['DOCUMENTS_FOLDER'], filename)


@main_blueprint.route('/document/upload', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'reviewer'])
def upload_document():
    form = CreateDocumentForm()

    if form.validate_on_submit():
        f = form.file.data
        fname = secure_filename(f.filename)
        fileext = fname.rsplit('.', 1)[1].lower()
        filename = "{title}_{time}.{ext}".format(
            title=form.tite.data,
            time=datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
            ext=fileext)

        f.save(os.path.join(current_app.config['DOCUMENTS_FOLDER'], filename))

        params = {'form_data': form.data, 'filename': filename}
        Document.create_document(params=params)

        return redirect(url_for('main.documents'))

    return render_template('main/upload.jinja2', form=form)


@main_blueprint.route('/document/delete/<document_id>')
@login_required
@roles_required(['admin', 'reviewer'])
def delete_document(document_id):
    Document.delete_by_id(document_id=document_id)
    return redirect(url_for('main.documents'))


@main_blueprint.route('/user/signed-out')
def signed_out():
    """Sign out landing page"""
    return render_template('flask_user/signed_out.html')


@main_blueprint.route('/documents')
@login_required
def documents():
    """documents Page"""
    query = Document.get_all()
    return render_template('main/documents.jinja2', documents=query)


@main_blueprint.route('/users', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def users():
    form = UpdateRoleForm()
    # form will not validate, so just checking if it's a post request
    # print(form.validate_on_submit())
    if request.method == 'POST' and form.user_id.data != current_user.id:
        UsersRoles.update_userrole(user_id=form.user_id.data, role_id=form.role_id.data)

    user_list = User.get_all()
    """About Page"""
    return render_template('main/users.jinja2', users=user_list, form=form)


@main_blueprint.route('/about')
@login_required
def about():
    """About Page"""
    return render_template('main/about.jinja2')
