from flask import Flask
from flask_assets import Environment
from webassets import Bundle

from app.configuration import AppConfiguration

# load the configuration
config = AppConfiguration()


def create_app():
    """Create and configure the Flask app

    Returns:
        Flask: the configured app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.flask_config)

    # register_extensions(app)
    register_blueprints(app)

    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('scss/site.scss', filters='libsass', output='site.css')
    assets.register('scss_all', scss)
    return app


# def register_extensions(app):
#     db.init_app(app)
#     migrate.init_app(app=app, db=db)
#     ma.init_app(app)

def register_blueprints(app):
    """Register blueprints for Flask app

    Args:
        app (Flask): Flask app to register for
    """
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .tad import tad_blueprint
    app.register_blueprint(tad_blueprint)
