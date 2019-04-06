from flask import render_template, Blueprint, url_for, redirect, send_from_directory
from flask_user import current_user, login_required, current_app
from app.models import Submission, Revision
import pycountry

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def splash():
    """Splash Page"""
    return redirect(url_for('user.login'))
    # return render_template('main/splash.jinja2')


@login_required
@main_blueprint.route('/home')
def index():
    """Home/Index Page"""
    return render_template('main/index.jinja2')


@login_required
@main_blueprint.route('/dashboard')
def dashboard():
    """Dashboard Page"""
    user = 'user'
    if current_user.has_roles('admin'):
        user = 'admin'
    else:
        if current_user.has_roles('reviewer'):
            user = 'reviewer'
    return render_template('main/dashboard.jinja2', user=user)


@login_required
@main_blueprint.route('/profile')
def profile():
    """Profile Page"""

    if current_user.pref_name == "":
        full_name = current_user.first_name + ' ' + current_user.middle_name + ' ' + current_user.last_name
    else:
        full_name = current_user.first_name + ' "' + current_user.pref_name + '" ' + current_user.middle_name + ' ' + current_user.last_name

    info = dict(name=full_name,
                department=current_user.department,
                email=current_user.email,
                net_id=current_user.net_id,
                msu_id=current_user.msu_id,
                birth_date=current_user.birth_date.strftime('%B %d, %Y'),  # Makes human redableS
                maiden_name=current_user.maiden_name,
                sec_email=current_user.sec_email,
                prim_phone=current_user.prim_phone,
                sec_phone=current_user.sec_phone,
                country=pycountry.countries.get(alpha_2=current_user.country).name,
                administrative_area=current_user.administrative_area,
                locality=current_user.locality,
                postal_code=current_user.postal_code,
                thoroughfare=current_user.thoroughfare,
                premise=current_user.premise)
    return render_template('main/profile.jinja2', data=info)


@login_required
@main_blueprint.route('/uploads/signatures/<filename>')
def uploads_signatures(filename):
    query = Submission.get_submission_by_signature(signature_filename=filename)
    if current_user.has_roles(['admin', 'viewer', 'reviewer', 'helper']) or query.id == query.user_id:
        return send_from_directory(current_app.config['SIGNATURE_FOLDER'], query.signature_file)
    else:
        return redirect(url_for('main.index'))


@login_required
@main_blueprint.route('/uploads/submissions/<filename>')
def uploads_submissions(filename):
    query = Revision.get_revision_by_filename(filename=filename)
    if current_user.has_roles(['admin', 'viewer', 'reviewer', 'helper']) or query.id == query.user_id:
        return send_from_directory(current_app.config['SUBMISSION_FOLDER'], query.file)
    else:
        return redirect(url_for('main.index'))


@login_required
@main_blueprint.route('/documents/<filename>')
def serve_documents(filename):
    return send_from_directory(current_app.config['DOCUMENT_FOLDER'], filename)


@main_blueprint.route('/user/signed-out')
def signed_out():
    """Sign out landing page"""
    return render_template('flask_user/signed_out.html')
