from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserMixin
from sqlalchemy_utils import ArrowType
import arrow
from flask_user import current_user

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    middle_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    msu_id = db.Column(db.Unicode(11), unique=True)
    net_id = db.Column(db.Unicode(8), unique=True)
    department = db.Column(db.Unicode(50), server_default=u'')

    sec_email = db.Column(db.Unicode(255), server_default=u'')
    prim_phone = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    sec_phone = db.Column(db.Unicode(50), server_default=u'')

    country = db.Column(db.Unicode(2), nullable=False, server_default=u'')
    administrative_area = db.Column(db.Unicode(50), nullable=False, server_default=u'')  # state/provinence
    locality = db.Column(db.Unicode(50), nullable=False, server_default=u'')  # city
    postal_code = db.Column(db.Unicode(50), nullable=False, server_default=u'')  # zip
    thoroughfare = db.Column(db.Unicode(50), nullable=False, server_default=u'')  # Street
    premise = db.Column(db.Unicode(50), nullable=False, server_default=u'')  # Apartment/box/etc

    pref_name = db.Column(db.Unicode(50), server_default=u'')

    maiden_name = db.Column(db.Unicode(50), server_default=u'')
    birth_date = db.Column(db.Date(), nullable=False)

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    def get_user_by_id(*, user_id=None):
        return User.query.filter(user_id == User.id).first()


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    text = db.Column(db.Unicode(50), nullable=False)
    state = db.Column(db.Boolean, default=False)


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.Unicode(), nullable=False)
    title = db.Column(db.Unicode(), nullable=False)
    description = db.Column(db.Unicode(), default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_document(*, params=None):
        document = Document(
            filename=params['filename'],
            title=params['form_data']['title'],
            description=params['form_data']['description']
        )

        document.save()
        return

    @staticmethod
    def delete_by_id(*, document_id=None):
        document = Document.query.filter(document_id == Document.id).first()
        db.session.delete(document)
        db.session.commit()
        return

    @staticmethod
    def get_all():
        return Document.query.all()


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id: Column = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    title = db.Column(db.Unicode(), nullable=False, server_default=u'')
    abstract = db.Column(db.Unicode(), nullable=False, server_default=u'')
    type = db.Column(db.Integer, nullable=False)
    release_type = db.Column(db.Integer, nullable=False)
    ww_length = db.Column(db.Integer, nullable=False)
    professor = db.Column(db.Unicode(8), nullable=False)
    signature_file = db.Column(db.Text, nullable=False)
    started = db.Column(ArrowType, default=arrow.now(), nullable=False)

    state = db.Column(db.Boolean, default=False, nullable=False)
    approved_date = db.Column(ArrowType)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_submission(*, params=None):
        submission = Submission(
            user_id=params['form_data']['user_id'],
            title=params['form_data']['title'],
            abstract=params['form_data']['abstract'],
            type=params['form_data']['type'],
            release_type=params['form_data']['release'],
            ww_length=params['form_data']['years'],
            professor=params['form_data']['professor'],
            signature_file=params['filename'],
        )

        submission.save()
        return submission.id

    @staticmethod
    def complete_submission_by_id(*, submission_id=None):
        submission = Submission.query.filter(submission_id == Submission.id).first()

        submission.state = True
        submission.approved_date = arrow.now()

        submission.save()
        return

    @staticmethod
    def get_submission_by_id(*, submission_id=None):
        return Submission.query.filter(submission_id == Submission.id).first()

    @staticmethod
    def get_submission_by_user_id(*, user_id=None):
        return Submission.query.filter(user_id == Submission.user_id).first()

    @staticmethod
    def get_all_submissions_by_user_id(*, user_id=None):
        # get ones that user owns
        own = Submission.query \
            .join(User, User.id == Submission.user_id) \
            .add_columns(User.id, User.first_name, User.last_name, Submission.id, Submission.state, Submission.title, Submission.started) \
            .filter(User.id == Submission.user_id) \
            .filter(Submission.user_id == User.id) \
            .filter(Submission.user_id == user_id) \
            .all()

        # get ones that user is listed as professor
        professors = Submission.query \
            .join(User, User.id == Submission.user_id) \
            .add_columns(User.id, User.first_name, User.last_name, Submission.id, Submission.state, Submission.title, Submission.started) \
            .filter(User.id == Submission.user_id) \
            .filter(Submission.user_id == User.id) \
            .filter(Submission.professor == current_user.net_id) \
            .all()
        return own + professors

    @staticmethod
    def get_all():
        return Submission.query \
                .join(User, User.id == Submission.user_id) \
                .add_columns(User.id, User.first_name, User.last_name, Submission.id, Submission.state, Submission.title, Submission.started) \
                .filter(User.id == Submission.user_id) \
                .filter(Submission.user_id == User.id).all()

    @staticmethod
    def get_submission_by_signature(*, signature_filename=None):
        return Submission.query.filter(signature_filename == Submission.signature_file).first()


class Revision(db.Model):
    __tablename__ = 'revisions'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer(), db.ForeignKey('submissions.id', ondelete='CASCADE'))
    submitted = db.Column(ArrowType, default=arrow.now())
    file = db.Column(db.Text)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_revision(*, params=None):
        revision = Revision(submission_id=params['submission_id'],
                            file=params['filename'])
        revision.save()
        return revision.id

    @staticmethod
    def get_all_revisions_by_submission_id(*, submission_id=None):
        return Revision.query.filter(Revision.submission_id == submission_id).all()

    @staticmethod
    def get_revision_by_id(*, revision_id=None):
        return Revision.query.filter(Revision.id == revision_id).first()

    @staticmethod
    def get_revision_by_filename(*, filename=None):
        return Revision.query.filter(Revision.file == filename).first()


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    revision_id = db.Column(db.Integer(), db.ForeignKey('revisions.id', ondelete='CASCADE'), unique=True, nullable=False)
    reviewed = db.Column(ArrowType, default=arrow.now())
    reviewer_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # 32 check boxes + comment box
    # check boxes will refer to the ones in the review form
    # new check boxes must be added at the end
    comments = db.Column(db.Unicode(), server_default=u'')
    check_1 = db.Column(db.Boolean, default=False, nullable=False)
    check_2 = db.Column(db.Boolean, default=False, nullable=False)
    check_3 = db.Column(db.Boolean, default=False, nullable=False)
    check_4 = db.Column(db.Boolean, default=False, nullable=False)
    check_5 = db.Column(db.Boolean, default=False, nullable=False)
    check_6 = db.Column(db.Boolean, default=False, nullable=False)
    check_7 = db.Column(db.Boolean, default=False, nullable=False)
    check_8 = db.Column(db.Boolean, default=False, nullable=False)
    check_9 = db.Column(db.Boolean, default=False, nullable=False)
    check_10 = db.Column(db.Boolean, default=False, nullable=False)
    check_11 = db.Column(db.Boolean, default=False, nullable=False)
    check_12 = db.Column(db.Boolean, default=False, nullable=False)
    check_13 = db.Column(db.Boolean, default=False, nullable=False)
    check_14 = db.Column(db.Boolean, default=False, nullable=False)
    check_15 = db.Column(db.Boolean, default=False, nullable=False)
    check_16 = db.Column(db.Boolean, default=False, nullable=False)
    check_17 = db.Column(db.Boolean, default=False, nullable=False)
    check_18 = db.Column(db.Boolean, default=False, nullable=False)
    check_19 = db.Column(db.Boolean, default=False, nullable=False)
    check_20 = db.Column(db.Boolean, default=False, nullable=False)
    check_21 = db.Column(db.Boolean, default=False, nullable=False)
    check_22 = db.Column(db.Boolean, default=False, nullable=False)
    check_23 = db.Column(db.Boolean, default=False, nullable=False)
    check_24 = db.Column(db.Boolean, default=False, nullable=False)
    check_25 = db.Column(db.Boolean, default=False, nullable=False)
    check_26 = db.Column(db.Boolean, default=False, nullable=False)
    check_27 = db.Column(db.Boolean, default=False, nullable=False)
    check_28 = db.Column(db.Boolean, default=False, nullable=False)
    check_29 = db.Column(db.Boolean, default=False, nullable=False)
    check_30 = db.Column(db.Boolean, default=False, nullable=False)
    check_31 = db.Column(db.Boolean, default=False, nullable=False)
    check_32 = db.Column(db.Boolean, default=False, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_review(*, params=None):
        review = Review(
            revision_id=params['revision_id'],
            reviewer_id=params['reviewer_id'],
            check_1=params['form_data']['check_1'],
            check_2=params['form_data']['check_3'],
            check_3=params['form_data']['check_3'],
            check_4=params['form_data']['check_4'],
            check_5=params['form_data']['check_5'],
            check_6=params['form_data']['check_6'],
            check_7=params['form_data']['check_7'],
            check_8=params['form_data']['check_8'],
            check_9=params['form_data']['check_9'],
            check_10=params['form_data']['check_10'],
            check_11=params['form_data']['check_11'],
            check_12=params['form_data']['check_12'],
            check_13=params['form_data']['check_13'],
            check_14=params['form_data']['check_14'],
            check_15=params['form_data']['check_15'],
            check_16=params['form_data']['check_16'],
            check_17=params['form_data']['check_17'],
            check_18=params['form_data']['check_18'],
            check_19=params['form_data']['check_19'],
            check_20=params['form_data']['check_20'],
            check_21=params['form_data']['check_21'],
            check_22=params['form_data']['check_22'],
            check_23=params['form_data']['check_23'],
            check_24=params['form_data']['check_24'],
            check_25=params['form_data']['check_25'],
            check_26=params['form_data']['check_26'],
            check_27=params['form_data']['check_27'],
            check_28=params['form_data']['check_28'],
            check_29=params['form_data']['check_29'],
            check_30=params['form_data']['check_30'],
            check_31=params['form_data']['check_31'],
            check_32=params['form_data']['check_32'],
            comments=params['form_data']['comments']
        )
        review.save()
        return

    @staticmethod
    def get_review_by_revision_id(*, revision_id=None):
        return Review.query.filter(Review.revision_id == revision_id).first()

    @staticmethod
    def get_reviews_by_revision_id(*, revision_id=None):
        return Review.query.filter(Review.revision_id == revision_id).first()
