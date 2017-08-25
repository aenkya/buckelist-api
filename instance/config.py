import os


class Config(object):
    """Parent configuration class"""
    DEBUG = False
    CSRF_ENABLED = True
    # ALT: <variable> = os.getenv('<env_var_name>')
    __SECRET = 'HeathLEDGERwasTHEBESTidc'
    # database with host configuration removed. Defaults to machine localhost
    __DB_NAME = os.getenv('DB_NAME') or "postgresql://localhost/bucketlist_api"
    BCRYPT_LOG_ROUNDS = 13
    SECRET_KEY = os.getenv('SECRET') or __SECRET
    AUTH_TOKEN_DURATION = os.getenv('TOKEN_DURATION') or 300
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_NAME') or __DB_NAME


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(Config):
    """Configurations for Testing with a separate test database"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/test_db"
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


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
