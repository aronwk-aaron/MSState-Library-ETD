import datetime
from flask import current_app
from flask_script import Command
import pycountry

from app import db
from app.models import User, Role


def init_db():
    """ Initialize the database."""
    print('Dropping all.')
    db.drop_all()
    print('Creating all.')
    db.create_all()
    print('Creating Admin User.')
    create_users()


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        print('Initializeing Database.')
        init_db()
        print('Database has been initialized.')


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')
    user_role = find_or_create_role('user', u'User')
    reviewer = find_or_create_role('reviewer', u'Reviewer')
    viewer = find_or_create_role('viewer', u'Viewer')
    helper = find_or_create_role('helper', u'Helper')


    # Add users
    admin_user = find_or_create_user(u'Admin', u'Admin', u'Admin', u'admin@library.msstate.edu', 'Password1', u'CSE', u'net001', u'000-000-000', 1970, 1, 1, u'16623257668', u'US', u'Mississippi', u'Mississippi State', u'39762', u'395 Hardy Rd', None, admin_role)

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, middle_name, last_name, email, password, department, net_id, msu_id, b_year, b_month, b_day, prim_phone, country=u'US', administrative_area=u'Mississippi', locality=u'Mississippi State', postal_code=u'39762', thoroughfare=u'395 Hardy Rd', premise=None, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        b_time = datetime.datetime(b_year, b_month, b_day)
        user = User(email=email,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    department=department,
                    net_id=net_id,
                    msu_id=msu_id,
                    birth_date=b_time.strftime('%B %d, %Y'),
                    prim_phone=prim_phone,
                    country=country,
                    administrative_area=administrative_area,
                    locality=locality,
                    postal_code=postal_code,
                    thoroughfare=thoroughfare,
                    premise=premise,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user


if __name__ == '__main__':
    init_db()

