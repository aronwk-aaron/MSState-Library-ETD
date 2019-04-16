from flask import Flask
from flask_assets import Environment
from webassets import Bundle

from app.forms.forms import CustomUserManager
from app.models import db, migrate, User
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

from app.models import User, Role, UsersRoles
from flask_user import user_registered

import click
from flask.cli import with_appcontext
import datetime
from flask_user import current_app


# Instantiate Flask extensions
ma = Marshmallow()
mail = Mail()
csrf_protect = CSRFProtect()
# db and migrate is instantiated in models.py


def create_app():
    """Create and configure the Flask app

    Returns:
        Flask: the configured app
    """

    app = Flask(__name__, instance_relative_config=True)

    # Load common settings
    app.config.from_object('app.settings')
    # Load environment specific settings
    app.config.from_object('app.local_settings')

    register_extensions(app)
    register_blueprints(app)
    # add the init_db command to flask cli
    app.cli.add_command(init_db)

    # Signal for giving users who register the 'user' role
    @user_registered.connect_via(app)
    def after_register_hook(sender, user, **extra):

        role = Role.query.filter_by(name="user").first()

        if role is None:
            role = Role(name="user")
            db.session.add(role)
            db.session.commit()

        user_role = UsersRoles(user_id=user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(app)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    return app


def register_extensions(app):
    """Register extensions for Flask app

    Args:
        app (Flask): Flask app to register for
    """
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    mail.init_app(app)
    csrf_protect.init_app(app)
    user_manager = CustomUserManager(app, db, User)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('scss/site.scss', filters='libsass', output='site.css')
    assets.register('scss_all', scss)

    db.create_all(app=app)


def register_blueprints(app):
    """Register blueprints for Flask app

    Args:
        app (Flask): Flask app to register for
    """
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .submissions import submissions_blueprint
    app.register_blueprint(submissions_blueprint, url_prefix='/submissions')
    from .revisions import revisions_blueprint
    app.register_blueprint(revisions_blueprint, url_prefix='/revisions')

    # from .auth import auth_blueprint
    # app.register_blueprint(auth_blueprint)


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    if app.debug: return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message')

# TODO: separate out into a commands file


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


