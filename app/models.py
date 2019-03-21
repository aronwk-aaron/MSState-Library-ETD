from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserMixin

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
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    middle_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

    msuid = db.Column(db.Text, nullable=False, unique=True)
    netid = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    professor = db.Column(db.Text, nullable=False)

    sec_email = db.Column(db.Text, nullable=False)

    prim_phone = db.Column(db.Text, nullable=False)
    sec_phone = db.Column(db.Text, nullable=False)

    country = db.Column(db.Text, nullable=False)
    administrative_area = db.Column(db.Text, nullable=False)
    locality = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.Text, nullable=False)
    thoroughfare = db.Column(db.Text, nullable=False)
    premise = db.Column(db.Text, nullable=False)

    pref_first_name = db.Column(db.Text)
    pref_middle_name = db.Column(db.Text)
    preflast_name = db.Column(db.Text)

    maiden_name = db.Column(db.Text, nullable=False)

    birth_date = db.Column(db.Text, nullable=False)


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
    text = db.Column(db.Text, nullable=False)
    state = db.Column(db.Boolean, default=False)


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    title = db.Column(db.Text)
    abstract = db.Column(db.Text)
    type = db.Column(db.Text)
    release_type = db.Column(db.Integer)
    ww_length = db.Column(db.Text)
    signature_file = db.Column(db.Text)

    state = db.Column(db.Boolean, default=False)
    approved_date = db.Column(db.Text)


class Revision(db.Model):
    __tablename__ = 'revisions'

    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer(), db.ForeignKey('submissions.id', ondelete='CASCADE'))
    file = db.Column(db.Text)
    rev_num = db.Column(db.Text)
    state = db.Column(db.Boolean, default=False)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review_ID = db.Column(db.Integer(), db.ForeignKey('reviews.id', ondelete='CASCADE'))
    reviewer_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    # put the checklist for it and figure out how to store checklist in a not dumb way
