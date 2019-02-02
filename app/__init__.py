from flask import Flask
from config import configs


def create_app(config_name='default'):
    """Create and configure the Flask app

    Args:
        config_name (str): the configuration name, defined in config.py

    Returns:
        Flask: the configured app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configs[config_name])

    # register_extensions(app)
    register_blueprints(app)

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
