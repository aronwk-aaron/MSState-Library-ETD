from flask import render_template, Blueprint

submissions_blueprint = Blueprint('submissions', __name__)


@submissions_blueprint.route('/')
def index():
    """Submissions Page
    view all submissions (based on role access level)
    """
    return render_template('submissions/index.jinja2')


@submissions_blueprint.route('/new')
def new():
    """New Submission Page
    Create new submission
    """
    return render_template('submissions/new.jinja2')


@submissions_blueprint.route('/submission/<id>')
def submission(id):
    """Submission Page
    View single submission with all revisions
    """
    return render_template('submissions/submission.jinja2', id=id)


@submissions_blueprint.route('/submission/<sub_id>/revision/<rev_id>')
def revision(sub_id, rev_id):
    """Revision Page
    View single revision of a submission
    """
    return render_template('submissions/revision.jinja2', sub_id=sub_id, rev_id=rev_id)


@submissions_blueprint.route('/review/<sub_id>/revision/<rev_id>')
def review(sub_id, rev_id):
    """Revision Page
    View single revision of a submission
    """
    return render_template('submissions/review.jinja2', sub_id=sub_id, rev_id=rev_id)
