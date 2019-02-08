import configparser
import os
from distutils.version import LooseVersion


class AppConfiguration(object):

    """Configuration Version"""
    CONFIG_VERSION = '1.0'

    def __init__(self):
        """Creates/Parses the config.ini"""
        # create/read the config.ini
        self.config_parser = self.reload_config()
        self.__update_config()

        # setup configuration
        self.mode = self.config_parser.get('FLASK', 'mode')

        # setup flask configuration
        self.flask_config = self.__FLASK_CONFIGS.get(self.mode, self.__DefaultFlaskConfig)
        self.flask_config.SECRET_KEY = self.__FLASK_CONFIGS.get('secret_key', 'SECRET_KEY_NOT_SET')

    def _create_config(self):
        """Creates a default configuration (*.ini) file

        Returns:
            config (ConfigParser): the config.ini parser
        """
        config = configparser.ConfigParser()

        # create the config
        config['CONFIG'] = {
            'version': self.CONFIG_VERSION
        }
        config['DATABASE'] = {
            'host': 'localhost',
            'name': 'msstate_etd',
            'user': 'msstate_etd',
            'pass': 'password',
            'type': 'postgresql'
        }
        config['FLASK'] = {
            'mode': 'default',
            'secret_key': 'SECRET_KEY_NOT_SET'
        }

        # write the config.
        config_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(config_path), 'config.ini')
        with open(config_path, 'w') as configfile:
            config.write(configfile)

        return config

    def reload_config(self):
        """Create/read the config.ini into ConfigParser

        Returns:
            the ConfigParser from config.ini
        """
        if not os.path.exists('config.ini'):
            print('creating new config...')
            config = self._create_config()
        else:
            print('loading config...')
            config = configparser.ConfigParser()
            config.read('config.ini')

        return config

    def get(self, *args):
        """Returns ConfigParser.get(*args)"""
        return self.config_parser.get(*args)

    def __update_config(self):
        """Checks if config.ini needs an update"""
        if LooseVersion(self.config_parser.get('CONFIG', 'version')) < LooseVersion(self.CONFIG_VERSION):
            print('updating config...')
            os.rename('config.ini', 'config.ini.backup')
            self.config_parser = self.reload_config()

    class __DefaultFlaskConfig(object):
        """Default/Production Flask Configuration"""
        DEBUG = False
        TESTING = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    class __DevelopmentFlaskConfig(__DefaultFlaskConfig):
        """Development/Debug Configuration"""
        DEBUG = True
        ASSETS_DEBUG = True
        SQLALCHEMY_ECHO = True

    class __TestingFlaskConfig(__DefaultFlaskConfig):
        """Testing Configuration"""
        TESTING = True

    # config map
    __FLASK_CONFIGS = {
        'dev': __DevelopmentFlaskConfig,
        'prod': __DefaultFlaskConfig,
        'test': __TestingFlaskConfig,
        'default': __DevelopmentFlaskConfig
    }
