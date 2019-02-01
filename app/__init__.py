from flask import Flask
from config import configs

def create_app(config_name='default'):
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
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)
