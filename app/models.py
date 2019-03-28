from sqlalchemy import Column
from sqlalchemy.sql import func
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
    administrative_area = db.Column(db.Unicode(50), nullable=False, server_default=u'')     # state/provinence
    locality = db.Column(db.Unicode(50), nullable=False, server_default=u'')                # city
    postal_code = db.Column(db.Unicode(50), nullable=False, server_default=u'')             # zip
    thoroughfare = db.Column(db.Unicode(50), nullable=False, server_default=u'')            # Street
    premise = db.Column(db.Unicode(50), nullable=False, server_default=u'')                 # Apartment/box/etc

    pref_name = db.Column(db.Unicode(50), server_default=u'')

    maiden_name = db.Column(db.Unicode(50), server_default=u'')
    birth_date = db.Column(db.Date(), nullable=False)

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))


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


class UsersProfessors(db.Model):
    __tablename__ = 'users_professors'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    Professor_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    text = db.Column(db.Text, nullable=False)
    state = db.Column(db.Boolean, default=False)


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id: Column = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    title = db.Column(db.Unicode(), nullable=False, server_default=u'')
    abstract = db.Column(db.Unicode(), nullable=False, server_default=u'')
    # TODO: Make Enum type for this
    type = db.Column(db.Integer, nullable=False)
    # TODO: Make Enum type for this
    release_type = db.Column(db.Integer, nullable=False)
    ww_length = db.Column(db.Integer, nullable=False)
    # TODO: figure out files for this
    signature_file = db.Column(db.Text)
    started = db.Column(db.DateTime(), server_default=func.now(), nullable=False)

    state = db.Column(db.Boolean, default=False, nullable=False)
    approved_date = db.Column(db.DateTime())


class Revision(db.Model):
    __tablename__ = 'revisions'

    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer(), db.ForeignKey('submissions.id', ondelete='CASCADE'))
    submitted = db.Column(db.DateTime(), server_default=func.now())
    # TODO: figure out files for this
    file = db.Column(db.Text)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    reviewed = db.Column(db.DateTime(), server_default=func.now())
    review_ID = db.Column(db.Integer(), db.ForeignKey('reviews.id', ondelete='CASCADE'))
    reviewer_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
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
