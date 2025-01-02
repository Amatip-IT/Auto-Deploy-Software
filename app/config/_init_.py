import os
from .settings import config_by_name

__all__ = ["get_config"]

def get_config():
    """
    Retrieves the appropriate configuration class based on the APP_ENV environment variable.

    :return: Configuration class (DevelopmentConfig, TestingConfig, ProductionConfig)
    """
    env = os.getenv("APP_ENV", "development").lower()
    config_class = config_by_name.get(env)

    if not config_class:
        raise ValueError(f"Invalid APP_ENV value: {env}. Must be one of: {', '.join(config_by_name.keys())}")

    return config_class
