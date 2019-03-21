from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import enum

from sqlalchemy_utils import ArrowType

import arrow
import random


db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = 'user'

    msuid = db.Column(db.Text, primary_key=True, nullable=False, unique=True)
    netid = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    professor = db.Column(db.Text, nullable=False)

    role = db.Column(db.Text, nullable=False)

    first_name = db.Column(db.Text, nullable=False)
    middle_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    prim_email = db.Column(db.Text, nullable=False)
    sec_email = db.Column(db.Text, nullable=False)

    prim_phone = db.Column(db.Text, nullable=False)
    sec_phone = db.Column(db.Text, nullable=False)

    country = db.Column(db.Text, nullable=False)
    administrative_area = db.Column(db.Text, nullable=False)
    locality = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.Text, nullable=False)
    thoroughfare = db.Column(db.Text, nullable=False)
    premise = db.Column(db.Text, nullable=False)

    preffirst_name = db.Column(db.Text)
    prefmiddle_name = db.Column(db.Text)
    preflast_name = db.Column(db.Text)

    maiden_name = db.Column(db.Text, nullable=False)

    birth_date = db.Column(db.Text, nullable=False)


class Notifications(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    netID = db.Column(db.Text, db.ForeignKey('user.netid'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    state = db.Column(db.Boolean, default=False)


class Submission(db.Model):
    __tablename__ = 'submission'

    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.Text, db.ForeignKey('user.netid'), nullable=False)
    title = db.Column(db.Text)
    abstract = db.Column(db.Text)
    type = db.Column(db.Text)
    release_type = db.Column(db.Integer)
    ww_length = db.Column(db.Text)
    signature_file = db.Column(db.Text)

    state = db.Column(db.Boolean, default=False)
    approved_date = db.Column(db.Text)


class Revision(db.Model):
    __tablename__ = 'revision'

    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Text)
    file = db.Column(db.Text)
    rev_num = db.Column(db.Text)
    state = db.Column(db.Boolean, default=False)


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    rev_id = db.Column(db.Integer)
    reviewer_netID = db.Column(db.Text, db.ForeignKey('user.netid'), nullable=False)
    # put the checklist for it and figure out how to store checklist in a not dumb way
