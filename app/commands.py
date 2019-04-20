import click
from flask.cli import with_appcontext
import datetime
from flask_user import current_app
from app import db
from app.models import Role, User


@click.command("init_db")
@with_appcontext
def init_db():
    """ Initialize the database."""

    print('Initializing Database.')
    print('Dropping all tables.')
    db.drop_all()
    print('Creating all tables.')
    db.create_all()
    create_users()
    print('Database has been initialized.')


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    print('Creating Roles.')
    admin_role = find_or_create_role('admin', u'Admin')  # 1
    user_role = find_or_create_role('user', u'User')  # 2
    reviewer = find_or_create_role('reviewer', u'Reviewer')  # 3
    viewer = find_or_create_role('viewer', u'Viewer')  # 4
    helper = find_or_create_role('helper', u'Helper')  # 5


    # Add users
    print('Creating Admin User.')
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
