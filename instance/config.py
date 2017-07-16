import os


class Config(object):
    """Parent configuration class"""
    DEBUG = False
    CSRF_ENABLED = True
    # ALT: <variable> = os.getenv('<env_var_name>')
    SECRET = 'HeathLEDGERwasTHEBESTidc'
    # database with host configuration removed. Defaults to machine localhost
    SQLALCHEMY_DATABASE_URI = "postgresql://bruce:Inline-360@localhost/bucketlist_api"


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing with a separate test database"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://bruce:Inline-360@localhost/test_db"
    DEBUG = True


class StagingConfig(Config):
    """Configurations for staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production"""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
