# config.py

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

    REDIS_URL = "redis://localhost"

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}